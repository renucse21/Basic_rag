import re
import uuid
from pathlib import Path
from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from ..config import get_settings
from ..rag.document_loader import load_pdf
from ..rag.text_splitter import split_pages
from ..schemas import UploadResponse

router = APIRouter(prefix="/api")
settings = get_settings()


def clean_filename(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", Path(value).name) or "document.pdf"


def _api_error_message(exc: Exception) -> str:
    message = str(exc).strip()
    if not message:
        return "Failed to process the PDF."
    lowered = message.lower()
    if any(token in lowered for token in ["connection", "connect", "11434", "refused"]):
        return "Ollama is unavailable. Start Ollama and make sure the configured models are installed: " + message
    return message


@router.post("/upload", response_model=UploadResponse)
async def upload(request: Request, file: UploadFile = File(...)):
    if request.app.state.vector_store is None:
        raise HTTPException(503, "Ollama is not configured or unavailable.")
    if file.content_type != "application/pdf" and not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported.")
    content = await file.read()
    if not content: raise HTTPException(400, "The uploaded file is empty.")
    if len(content) > settings.max_upload_size_mb * 1024 * 1024:
        raise HTTPException(413, f"File exceeds {settings.max_upload_size_mb} MB.")
    filename = clean_filename(file.filename or "document.pdf")
    document_id = uuid.uuid4().hex
    path = settings.upload_path / f"{uuid.uuid4().hex}_{filename}"
    try:
        path.write_bytes(content)
        chunks = split_pages(load_pdf(path), settings.chunk_size, settings.chunk_overlap)
        if not chunks: raise ValueError("The PDF contains no extractable text.")
        count = request.app.state.vector_store.add(document_id, filename, chunks)
        return {"success": True, "message": "PDF indexed successfully.", "document_id": document_id,
                "filename": filename, "chunks": count}
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    except Exception as exc:
        raise HTTPException(500, _api_error_message(exc)) from exc
    finally:
        path.unlink(missing_ok=True)
