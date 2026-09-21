from langchain_ollama import ChatOllama
from ..config import Settings
from .vector_store import VectorStore


class QAService:
    def __init__(self, settings: Settings, store: VectorStore):
        self.settings, self.store = settings, store
        self.model = ChatOllama(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            base_url=settings.ollama_base_url,
        )

    def answer(self, question: str, document_id: str):
        matches = self.store.search(question, document_id, self.settings.top_k)
        if not matches:
            return "I could not find the answer in the uploaded document.", []
        context = "\n\n".join(f"[Source {i + 1}] {text}" for i, (text, _) in enumerate(matches))
        response = self.model.invoke(
            "You are a document question-answering assistant. Answer the user's question "
            "using ONLY the information in the provided context. Do not use outside knowledge "
            "or make up information. If the answer cannot be found in the context, respond "
            "exactly: 'I could not find the answer in the uploaded document.' "
            "When possible, provide a concise and clear answer and cite sources as [Source N].\n\n"
            "Context:\n" + context + "\n\nQuestion:\n" + question
        )
        sources = [{"filename": str(meta["filename"]), "page": int(meta["page"])} for _, meta in matches]
        return str(response.content), sources
