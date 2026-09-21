from typing import Any
import chromadb
from ..config import Settings
from .embeddings import EmbeddingService


class VectorStore:
    def __init__(self, settings: Settings, embeddings: EmbeddingService):
        self.embeddings = embeddings
        client = chromadb.PersistentClient(path=str(settings.chroma_path))
        self.collection = client.get_or_create_collection("pdf_chunks", metadata={"hnsw:space": "cosine"})

    def add(self, document_id: str, filename: str, chunks: list[dict]):
        ids = [f"{document_id}-{i}" for i in range(len(chunks))]
        self.collection.delete(where={"document_id": document_id})
        self.collection.add(ids=ids, documents=[x["text"] for x in chunks],
                            embeddings=self.embeddings.embed([x["text"] for x in chunks]),
                            metadatas=[{"document_id": document_id, "filename": filename,
                                        "page": x["page"], "chunk": i} for i, x in enumerate(chunks)])
        return len(chunks)

    def search(self, question: str, document_id: str, top_k: int):
        result = self.collection.query(query_embeddings=[self.embeddings.embed_query(question)],
                                       n_results=top_k, where={"document_id": document_id},
                                       include=["documents", "metadatas"])
        return list(zip((result.get("documents") or [[]])[0], (result.get("metadatas") or [[]])[0]))
