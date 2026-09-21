from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .rag.embeddings import EmbeddingService
from .rag.qa_chain import QAService
from .rag.vector_store import VectorStore
from .routes.chat import router as chat_router
from .routes.upload import router as upload_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.vector_store = VectorStore(settings, EmbeddingService(settings))
        app.state.qa_service = QAService(settings, app.state.vector_store)
    except RuntimeError:
        app.state.vector_store = None
        app.state.qa_service = None
    yield


app = FastAPI(title="PDF RAG Assistant API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(upload_router)
app.include_router(chat_router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
