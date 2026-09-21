from langchain_ollama import OllamaEmbeddings
from ..config import Settings


class EmbeddingService:
    def __init__(self, settings: Settings):
        self.client = OllamaEmbeddings(
            model=settings.embedding_model,
            base_url=settings.ollama_base_url,
        )

    def embed(self, texts: list[str]): return self.client.embed_documents(texts)
    def embed_query(self, text: str): return self.client.embed_query(text)
