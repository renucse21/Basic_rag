from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_embedding_model: str = "text-embedding-3-small"
    openai_chat_model: str = "gpt-4o-mini"
    openai_chat_temperature: float = 0.2
    chunk_size: int = 1000
    chunk_overlap: int = 150
    top_k: int = 4
    max_upload_size_mb: int = 20
    chroma_persist_directory: str = "./data/chroma"
    upload_directory: str = "./data/uploads"
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def chroma_path(self) -> Path:
        return Path(self.chroma_persist_directory)

    @property
    def upload_path(self) -> Path:
        return Path(self.upload_directory)

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.chroma_path.mkdir(parents=True, exist_ok=True)
    settings.upload_path.mkdir(parents=True, exist_ok=True)
    return settings
