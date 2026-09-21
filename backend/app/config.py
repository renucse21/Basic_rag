from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "llama3.2"
    embedding_model: str = "nomic-embed-text"
    llm_temperature: float = 0.2
    chunk_size: int = 1000
    chunk_overlap: int = 150
    top_k: int = 4
    max_upload_size_mb: int = 20
    chroma_persist_directory: str = "./data/chroma"
    upload_directory: str = "./data/uploads"
    cors_origins: str = "http://localhost:5173"
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def allowed_origins(self): return [x.strip() for x in self.cors_origins.split(",") if x.strip()]
    @property
    def chroma_path(self): return Path(self.chroma_persist_directory)
    @property
    def upload_path(self): return Path(self.upload_directory)


@lru_cache
def get_settings():
    settings = Settings()
    settings.chroma_path.mkdir(parents=True, exist_ok=True)
    settings.upload_path.mkdir(parents=True, exist_ok=True)
    return settings
