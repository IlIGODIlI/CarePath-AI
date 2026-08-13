"""Production medical knowledge retrieval and evidence synthesis engine."""

from __future__ import annotations

import math
import re
import time
from dataclasses import dataclass
from typing import Any, Iterable

from app.core.config import settings
from app.core.interfaces import (
    KnowledgeRetrievalService,
    ServiceAvailability,
    ServiceHealthStatus,
)
from app.core.logging import get_logger
from app.core.validation import validate_text_input, validate_top_k
from app.schemas.rag import DocumentChunk, RAGQueryResponse

logger = get_logger(__name__)


@dataclass(frozen=True)
class _KnowledgeDocument:
    """Canonical internal representation of a medical knowledge document."""

    document_id: str
    title: str
    source: str
    content: str
    metadata: dict[str, str]


@dataclass(frozen=True)
class _ScoredDocument:
    """Knowledge document with retrieval score."""

    document: _KnowledgeDocument
    score: float


class RAGKnowledgeEngine(KnowledgeRetrievalService):
    """
    Evidence retrieval engine for medical knowledge.

    Retrieval hierarchy:
        ChromaDB semantic retrieval
                    ↓
        deterministic lexical fallback

    The engine retrieves and summarizes supplied evidence. It does not
    generate unsupported patient-specific diagnoses or treatment plans.
    """

    _SERVICE_NAME = "CarePath RAG Knowledge Engine"
    _SERVICE_VERSION = "1.0.0"
    _COLLECTION_NAME = "medical_guidelines"

    KNOWLEDGE_BASE: tuple[_KnowledgeDocument, ...] = (
        _KnowledgeDocument(
            document_id="guideline_pneumonia_2024",
            title=(
                "ATS/IDSA Clinical Practice Guidelines for "
                "Community-Acquired Pneumonia"
            ),
            source="American Thoracic Society / IDSA",
            content=(
                "For outpatient community-acquired pneumonia in adults "
                "without comorbidities, empirical amoxicillin 1g TID or "
                "doxycycline 100mg BID is strongly recommended. For patients "
                "with comorbidities or recent antibiotic use, combination "
                "therapy with beta-lactam and macrolide or respiratory "
                "fluoroquinolone is indicated."
            ),
            metadata={
                "domain": "respiratory",
                "condition": "community-acquired pneumonia",
                "year": "2024",
            },
        ),
        _KnowledgeDocument(
            document_id="guideline_diabetes_2024",
            title="ADA Standards of Care in Diabetes Management",
            source="American Diabetes Association",
            content=(
                "First-line therapy for type 2 diabetes includes metformin "
                "and comprehensive lifestyle modification. If HbA1c remains "
                "above target, add SGLT2 inhibitor or GLP-1 receptor agonist, "
                "particularly in patients with established ASCVD, heart "
                "failure, or chronic kidney disease."
            ),
            metadata={
                "domain": "endocrinology",
                "condition": "type 2 diabetes",
                "year": "2024",
            },
        ),
        _KnowledgeDocument(
            document_id="guideline_hypertension_2024",
            title="ACC/AHA Guideline for Management of High Blood Pressure",
            source="ACC/AHA Clinical Guidelines",
            content=(
                "First-line pharmacological agents for Stage 1 or Stage 2 "
                "hypertension include thiazide diuretics, calcium channel "
                "blockers, or ACE inhibitors/ARBs. Dual combination therapy "
                "is recommended for patients with Stage 2 hypertension "
                "(BP >140/90 mmHg)."
            ),
            metadata={
                "domain": "cardiology",
                "condition": "hypertension",
                "year": "2024",
            },
        ),
    )

    _TOKEN_PATTERN = re.compile(
        r"[a-zA-Z0-9]+(?:[-'][a-zA-Z0-9]+)*"
    )

    _STOP_WORDS = frozenset(
        {
            "a",
            "an",
            "and",
            "are",
            "as",
            "at",
            "be",
            "by",
            "for",
            "from",
            "how",
            "i",
            "in",
            "is",
            "it",
            "me",
            "of",
            "on",
            "or",
            "the",
            "to",
            "what",
            "when",
            "with",
        }
    )

    def __init__(self) -> None:
        self._client: Any | None = None
        self._collection: Any | None = None
        self._chroma_ready = False
        self._initialization_error: str | None = None

        self._initialize_vector_store()

    # ------------------------------------------------------------------
    # Service interface
    # ------------------------------------------------------------------

    def health_check(self) -> ServiceHealthStatus:
        if self._chroma_ready:
            return ServiceHealthStatus(
                availability=ServiceAvailability.AVAILABLE,
                backend="chromadb",
                message="ChromaDB vector store is available.",
            )

        return ServiceHealthStatus(
            availability=ServiceAvailability.DEGRADED,
            backend="lexical_fallback",
            message=(
                "ChromaDB is unavailable. "
                "Deterministic lexical retrieval is active."
            ),
        )

    def get_service_info(self) -> dict:
        health = self.health_check()

        try:
            indexed_documents = (
                self._collection.count()
                if self._chroma_ready and self._collection
                else len(self.KNOWLEDGE_BASE)
            )
        except Exception:
            indexed_documents = len(self.KNOWLEDGE_BASE)

        return {
            "name": self._SERVICE_NAME,
            "version": self._SERVICE_VERSION,
            "status": health.availability.value,
            "backend": health.backend,
            "collection": self._COLLECTION_NAME,
            "indexed_documents": indexed_documents,
            "knowledge_base_documents": len(self.KNOWLEDGE_BASE),
            "max_top_k": 10,
        }

    # ------------------------------------------------------------------
    # Vector store
    # ------------------------------------------------------------------

    def _initialize_vector_store(self) -> None:
        """Initialize ChromaDB and synchronize the supplied knowledge base."""
        try:
            import chromadb

            self._client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIRECTORY,
            )

            self._collection = (
                self._client.get_or_create_collection(
                    name=self._COLLECTION_NAME,
                    metadata={
                        "description": (
                            "CarePath AI medical guideline "
                            "retrieval collection"
                        ),
                    },
                )
            )

            self._synchronize_knowledge_base()

            self._chroma_ready = True
            self._initialization_error = None

            logger.info(
                "ChromaDB RAG collection initialized with %d documents.",
                self._collection.count(),
            )

        except Exception as exc:
            self._chroma_ready = False
            self._client = None
            self._collection = None
            self._initialization_error = str(exc)

            logger.warning(
                "ChromaDB unavailable; using lexical retrieval fallback: %s",
                exc,
            )

    def _synchronize_knowledge_base(self) -> None:
        if self._collection is None:
            raise RuntimeError(
                "ChromaDB collection is not initialized."
            )

        for document in self.KNOWLEDGE_BASE:
            existing = self._collection.get(
                ids=[document.document_id],
            )

            existing_ids = existing.get("ids", [])

            metadata = {
                "title": document.title,
                "source": document.source,
                **document.metadata,
            }

            if document.document_id in existing_ids:
                self._collection.upsert(
                    ids=[document.document_id],
                    documents=[document.content],
                    metadatas=[metadata],
                )
            else:
                self._collection.add(
                    ids=[document.document_id],
                    documents=[document.content],
                    metadatas=[metadata],
                )

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def query_guidelines(
        self,
        query: str,
        top_k: int = 3,
    ) -> RAGQueryResponse:
        """Retrieve the most relevant available medical evidence."""
        validate_text_input(
            query,
            min_len=1,
            max_len=4096,
        )

        validate_top_k(
            top_k,
            min_k=1,
            max_k=10,
        )

        started = time.perf_counter()

        normalized_query = " ".join(
            query.split()
        ).strip()

        retrieved: list[DocumentChunk] = []

        if self._chroma_ready:
            try:
                retrieved = self._query_chromadb(
                    normalized_query,
                    top_k,
                )
            except Exception as exc:
                logger.exception(
                    "ChromaDB retrieval failed; "
                    "falling back to lexical retrieval."
                )

                retrieved = []
                self._initialization_error = str(exc)

        if not retrieved:
            retrieved = self._query_lexical(
                normalized_query,
                top_k,
            )

        retrieved = self._re_rank(
            query=normalized_query,
            documents=retrieved,
            top_k=top_k,
        )

        answer = self._build_evidence_grounded_answer(
            query=normalized_query,
            documents=retrieved,
        )

        citations = [
            f"{chunk.title} — {chunk.source}"
            for chunk in retrieved
        ]

        confidence = self._calculate_response_confidence(
            retrieved
        )

        elapsed = round(
            time.perf_counter() - started,
            4,
        )

        backend = (
            "chromadb"
            if self._chroma_ready and retrieved
            else "lexical_fallback"
        )

        return RAGQueryResponse(
            query=normalized_query,
            retrieved_chunks=retrieved,
            synthesized_guideline_answer=answer,
            citations=citations,
            processing_time_seconds=elapsed,
            backend=backend,
            evidence_found=bool(retrieved),
            confidence_score=confidence,
        )

    # ------------------------------------------------------------------
    # ChromaDB retrieval
    # ------------------------------------------------------------------

    def _query_chromadb(
        self,
        query: str,
        top_k: int,
    ) -> list[DocumentChunk]:
        if self._collection is None:
            return []

        result = self._collection.query(
            query_texts=[query],
            n_results=min(
                top_k,
                self._collection.count(),
            ),
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        documents = result.get(
            "documents",
            [[]],
        )[0]

        metadatas = result.get(
            "metadatas",
            [[]],
        )[0]

        distances = result.get(
            "distances",
            [[]],
        )[0]

        ids = result.get(
            "ids",
            [[]],
        )[0]

        chunks: list[DocumentChunk] = []

        for index, (
            document_id,
            content,
            metadata,
        ) in enumerate(
            zip(
                ids,
                documents,
                metadatas,
            ),
            start=1,
        ):
            distance = (
                float(distances[index - 1])
                if index - 1 < len(distances)
                else 1.0
            )

            score = self._distance_to_score(
                distance
            )

            metadata = metadata or {}

            chunks.append(
                DocumentChunk(
                    chunk_id=str(document_id),
                    title=str(
                        metadata.get(
                            "title",
                            "Medical Guideline",
                        )
                    ),
                    content=str(content),
                    source=str(
                        metadata.get(
                            "source",
                            "Medical Literature",
                        )
                    ),
                    relevance_score=score,
                    rank=index,
                    metadata={
                        str(key): str(value)
                        for key, value in metadata.items()
                    },
                )
            )

        return chunks

    @staticmethod
    def _distance_to_score(
        distance: float,
    ) -> float:
        """Convert vector distance into a bounded relevance score."""
        if not math.isfinite(distance):
            return 0.0

        distance = max(
            distance,
            0.0,
        )

        return round(
            1.0 / (1.0 + distance),
            4,
        )

    # ------------------------------------------------------------------
    # Lexical fallback
    # ------------------------------------------------------------------

    def _query_lexical(
        self,
        query: str,
        top_k: int,
    ) -> list[DocumentChunk]:
        query_tokens = self._tokenize(query)

        if not query_tokens:
            return []

        scored: list[_ScoredDocument] = []

        for document in self.KNOWLEDGE_BASE:
            score = self._lexical_score(
                query_tokens,
                document,
            )

            if score <= 0.0:
                continue

            scored.append(
                _ScoredDocument(
                    document=document,
                    score=score,
                )
            )

        scored.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        chunks: list[DocumentChunk] = []

        for rank, item in enumerate(
            scored[:top_k],
            start=1,
        ):
            document = item.document

            chunks.append(
                DocumentChunk(
                    chunk_id=document.document_id,
                    title=document.title,
                    content=document.content,
                    source=document.source,
                    relevance_score=round(
                        item.score,
                        4,
                    ),
                    rank=rank,
                    metadata=document.metadata,
                )
            )

        return chunks

    def _lexical_score(
        self,
        query_tokens: set[str],
        document: _KnowledgeDocument,
    ) -> float:
        searchable_text = " ".join(
            (
                document.title,
                document.content,
                document.source,
                " ".join(
                    document.metadata.values()
                ),
            )
        ).lower()

        document_tokens = self._tokenize(
            searchable_text
        )

        if not document_tokens:
            return 0.0

        overlap = query_tokens.intersection(
            document_tokens
        )

        if not overlap:
            return 0.0

        coverage = (
            len(overlap)
            / len(query_tokens)
        )

        density = (
            len(overlap)
            / max(
                len(document_tokens),
                1,
            )
        )

        score = (
            0.85 * coverage
            + 0.15 * min(
                density * 20,
                1.0,
            )
        )

        return min(
            max(score, 0.0),
            1.0,
        )

    # ------------------------------------------------------------------
    # Re-ranking
    # ------------------------------------------------------------------

    def _re_rank(
        self,
        query: str,
        documents: list[DocumentChunk],
        top_k: int,
    ) -> list[DocumentChunk]:
        query_tokens = self._tokenize(query)

        scored: list[
            tuple[float, DocumentChunk]
        ] = []

        for document in documents:
            title_tokens = self._tokenize(
                document.title
            )

            query_title_overlap = len(
                query_tokens.intersection(
                    title_tokens
                )
            )

            title_bonus = min(
                query_title_overlap * 0.04,
                0.12,
            )

            final_score = min(
                document.relevance_score
                + title_bonus,
                1.0,
            )

            scored.append(
                (
                    final_score,
                    document,
                )
            )

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        result: list[DocumentChunk] = []

        for rank, (
            score,
            document,
        ) in enumerate(
            scored[:top_k],
            start=1,
        ):
            result.append(
                document.model_copy(
                    update={
                        "relevance_score": round(
                            score,
                            4,
                        ),
                        "rank": rank,
                    }
                )
            )

        return result

    # ------------------------------------------------------------------
    # Evidence synthesis
    # ------------------------------------------------------------------

    @staticmethod
    def _build_evidence_grounded_answer(
        query: str,
        documents: list[DocumentChunk],
    ) -> str:
        """
        Build an extractive evidence summary.

        Every substantive statement comes from retrieved evidence.
        """
        if not documents:
            return (
                "No sufficiently relevant medical guideline evidence "
                "was retrieved for this query. A clinician or an "
                "appropriately sourced medical knowledge base should be "
                "consulted rather than inferring an answer from missing "
                "evidence."
            )

        sections: list[str] = [
            f"Retrieved evidence relevant to: {query}"
        ]

        for index, document in enumerate(
            documents,
            start=1,
        ):
            sections.append(
                (
                    f"[Evidence {index}] "
                    f"{document.title} "
                    f"({document.source}): "
                    f"{document.content}"
                )
            )

        sections.append(
            (
                "This retrieval output summarizes the supplied guideline "
                "evidence and is not a patient-specific diagnosis or "
                "treatment recommendation."
            )
        )

        return "\n\n".join(sections)

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def _calculate_response_confidence(
        self,
        documents: list[DocumentChunk],
    ) -> float:
        if not documents:
            return 0.0

        scores = [
            document.relevance_score
            for document in documents
        ]

        weighted = sum(
            score / (index + 1)
            for index, score in enumerate(scores)
        )

        normalization = sum(
            1.0 / (index + 1)
            for index in range(len(scores))
        )

        if normalization == 0:
            return 0.0

        return round(
            min(
                max(
                    weighted / normalization,
                    0.0,
                ),
                1.0,
            ),
            4,
        )

    def _tokenize(
        self,
        text: str,
    ) -> set[str]:
        tokens = {
            token.lower()
            for token in self._TOKEN_PATTERN.findall(text)
        }

        return {
            token
            for token in tokens
            if token not in self._STOP_WORDS
            and len(token) > 1
        }


rag_engine = RAGKnowledgeEngine()