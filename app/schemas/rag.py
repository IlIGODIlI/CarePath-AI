"""Medical Knowledge RAG Schemas."""
from typing import List
from pydantic import BaseModel, Field


class RAGQueryRequest(BaseModel):
    query: str = Field(description="Clinical query or symptom presentation")
    top_k: int = Field(default=3, ge=1, le=10)


class DocumentChunk(BaseModel):
    chunk_id: str
    title: str
    content: str
    source: str
    relevance_score: float


class RAGQueryResponse(BaseModel):
    query: str
    retrieved_chunks: List[DocumentChunk] = Field(default_factory=list)
    synthesized_guideline_answer: str
    citations: List[str] = Field(default_factory=list)
    processing_time_seconds: float
