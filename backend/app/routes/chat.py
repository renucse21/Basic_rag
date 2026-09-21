from fastapi import APIRouter, HTTPException, Request

from ..schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/api")


def _api_error_message(exc: Exception) -> str:
    message = str(exc).strip()
    if not message:
        return "The AI service could not answer the question."
    lowered = message.lower()
    if any(token in lowered for token in ["connection", "connect", "11434", "refused"]):
        return "Ollama is unavailable. Start Ollama and make sure the configured models are installed: " + message
    return message


@router.post("/chat", response_model=ChatResponse)
def chat(request: Request, payload: ChatRequest):
    if request.app.state.qa_service is None:
        raise HTTPException(503, "Ollama is not configured or unavailable.")
    try:
        answer, sources = request.app.state.qa_service.answer(payload.question.strip(), payload.document_id)
        unique = {(source["filename"], source["page"]): source for source in sources}
        return {"answer": answer, "sources": list(unique.values())}
    except Exception as exc:
        raise HTTPException(502, _api_error_message(exc)) from exc
