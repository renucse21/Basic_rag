from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    success: bool
    message: str
    document_id: str
    filename: str
    chunks: int


class ChatRequest(BaseModel):
    document_id: str = Field(..., min_length=1)
    question: str = Field(..., min_length=2, max_length=4000)


class Source(BaseModel):
    filename: str
    page: int | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
