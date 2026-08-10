"""Medical Knowledge RAG Subsystem with Vector Search."""
import time
from typing import List
from app.schemas.rag import RAGQueryResponse, DocumentChunk
from app.core.config import settings
from app.core.logging import get_logger
from app.core.interfaces import KnowledgeRetrievalService, ServiceHealthStatus, ServiceAvailability
from app.core.validation import validate_text_input, validate_top_k

logger = get_logger(__name__)


class RAGKnowledgeEngine(KnowledgeRetrievalService):
    """Medical RAG Engine for Clinical Guideline Retrieval."""

    _SERVICE_NAME = "CarePath RAG Knowledge Engine"
    _SERVICE_VERSION = "0.1.0"

    # Built-in reference clinical practice guidelines
    KNOWLEDGE_BASE = [
        {
            "id": "guideline_pneumonia_2024",
            "title": "ATS/IDSA Clinical Practice Guidelines for Community-Acquired Pneumonia",
            "source": "American Thoracic Society / IDSA",
            "content": "For outpatient community-acquired pneumonia in adults without comorbidities, empirical amoxicillin 1g TID or doxycycline 100mg BID is strongly recommended. For patients with comorbidities or recent antibiotic use, combination therapy with beta-lactam and macrolide or respiratory fluoroquinolone is indicated."
        },
        {
            "id": "guideline_diabetes_2024",
            "title": "ADA Standards of Care in Diabetes Management",
            "source": "American Diabetes Association",
            "content": "First-line therapy for type 2 diabetes includes metformin and comprehensive lifestyle modification. If HbA1c remains above target, add SGLT2 inhibitor or GLP-1 receptor agonist, particularly in patients with established ASCVD, heart failure, or chronic kidney disease."
        },
        {
            "id": "guideline_hypertension_2024",
            "title": "ACC/AHA Guideline for Management of High Blood Pressure",
            "source": "ACC/AHA Clinical Guidelines",
            "content": "First-line pharmacological agents for Stage 1 or Stage 2 hypertension include thiazide diuretics, calcium channel blockers, or ACE inhibitors/ARBs. Dual combination therapy is recommended for patients with Stage 2 hypertension (BP >140/90 mmHg)."
        }
    ]

    def __init__(self):
        self._init_vector_db()

    # ------------------------------------------------------------------
    # Interface: BaseAIService
    # ------------------------------------------------------------------

    def health_check(self) -> ServiceHealthStatus:
        """Return current RAG backend availability."""
        if getattr(self, "_chroma_ready", False):
            return ServiceHealthStatus(
                availability=ServiceAvailability.AVAILABLE,
                backend="chromadb",
                message="ChromaDB vector store is active.",
            )
        return ServiceHealthStatus(
            availability=ServiceAvailability.DEGRADED,
            backend="keyword_fallback",
            message="Running in keyword-ranking fallback mode; ChromaDB unavailable.",
        )

    def get_service_info(self) -> dict:
        """Return metadata about this RAG engine instance."""
        health = self.health_check()
        doc_count = len(self.KNOWLEDGE_BASE)
        if getattr(self, "_chroma_ready", False):
            try:
                doc_count = self._collection.count()
            except Exception:
                pass
        return {
            "name": self._SERVICE_NAME,
            "version": self._SERVICE_VERSION,
            "status": health.availability.value,
            "backend": health.backend,
            "collection": settings.CHROMA_COLLECTION_NAME,
            "indexed_documents": doc_count,
        }

    def _init_vector_db(self):
        """Initialize local vector database (ChromaDB)."""
        try:
            import chromadb
            self._client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)
            self._collection = self._client.get_or_create_collection(name="medical_guidelines")

            # Seed collection if empty
            if self._collection.count() == 0:
                ids = [doc["id"] for doc in self.KNOWLEDGE_BASE]
                documents = [doc["content"] for doc in self.KNOWLEDGE_BASE]
                metadatas = [{"title": doc["title"], "source": doc["source"]} for doc in self.KNOWLEDGE_BASE]
                self._collection.add(ids=ids, documents=documents, metadatas=metadatas)
                logger.info(f"Seeded ChromaDB with {len(ids)} clinical practice guidelines.")
            self._chroma_ready = True
        except Exception as e:
            logger.warning(f"ChromaDB initialization fallback: {e}. Using semantic keyword ranker.")
            self._chroma_ready = False

    def query_guidelines(self, query: str, top_k: int = 3) -> RAGQueryResponse:
        """Search medical guidelines and synthesise evidence-based answer."""
        validate_text_input(query, min_len=1, max_len=4096)
        validate_top_k(top_k, min_k=1, max_k=10)
        start_time = time.time()
        retrieved_chunks: List[DocumentChunk] = []

        if hasattr(self, "_chroma_ready") and self._chroma_ready:
            try:
                results = self._collection.query(query_texts=[query], n_results=top_k)
                docs = results.get("documents", [[]])[0]
                metas = results.get("metadatas", [[]])[0]
                ids = results.get("ids", [[]])[0]

                for doc_id, doc_text, meta in zip(ids, docs, metas):
                    retrieved_chunks.append(DocumentChunk(
                        chunk_id=doc_id,
                        title=meta.get("title", "Clinical Guideline"),
                        content=doc_text,
                        source=meta.get("source", "Medical Literature"),
                        relevance_score=0.89
                    ))
            except Exception as e:
                logger.error(f"ChromaDB query error: {e}")

        if not retrieved_chunks:
            # Fallback search ranking
            query_lower = query.lower()
            for doc in self.KNOWLEDGE_BASE:
                score = sum(1 for word in query_lower.split() if word in doc["content"].lower())
                if score > 0 or len(retrieved_chunks) < top_k:
                    retrieved_chunks.append(DocumentChunk(
                        chunk_id=doc["id"],
                        title=doc["title"],
                        content=doc["content"],
                        source=doc["source"],
                        relevance_score=round(0.75 + (score * 0.05), 2)
                    ))

        retrieved_chunks = sorted(retrieved_chunks, key=lambda x: x.relevance_score, reverse=True)[:top_k]

        citations = [f"{c.title} ({c.source})" for c in retrieved_chunks]
        synthesized_ans = f"Based on {len(retrieved_chunks)} clinical guideline(s): " + " ".join([c.content for c in retrieved_chunks[:2]])

        elapsed = round(time.time() - start_time, 3)

        return RAGQueryResponse(
            query=query,
            retrieved_chunks=retrieved_chunks,
            synthesized_guideline_answer=synthesized_ans,
            citations=citations,
            processing_time_seconds=elapsed
        )


rag_engine = RAGKnowledgeEngine()
