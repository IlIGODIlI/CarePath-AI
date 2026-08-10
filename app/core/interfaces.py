"""Abstract Service Interfaces for CarePath AI Modules.

Every concrete AI engine (OCR, Vision, NLP, RAG, CarePathEngine) must
implement the matching interface so that:

1.  The ``CarePathEngine`` and test harnesses can depend on the interface,
    not the concrete implementation (Dependency Inversion Principle).
2.  ``health_check()`` gives a uniform way to verify engine readiness
    across all modules without coupling to HTTP machinery.
3.  ``get_service_info()`` provides introspection metadata useful for
    logging, monitoring, and the ``/api/v1/status`` endpoint.

Usage
-----
Concrete engines subclass the appropriate interface and are registered with
``@dataclasses.dataclass`` on the ``ServiceHealthStatus`` they return.

    class MyOCREngine(TextExtractionService):
        def extract_text(self, image_bytes, filename):
            ...
        def health_check(self):
            ...
        def get_service_info(self):
            ...
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Health Status
# ---------------------------------------------------------------------------


class ServiceAvailability(str, Enum):
    """Coarse-grained availability classification for AI services."""

    AVAILABLE = "available"
    DEGRADED = "degraded"      # Running but with reduced capability (e.g. fallback mode)
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class ServiceHealthStatus:
    """Immutable snapshot of an AI service's readiness.

    Parameters
    ----------
    availability:
        One of ``ServiceAvailability`` values.
    message:
        Optional human-readable explanation (e.g. "Using keyword fallback — ChromaDB unavailable").
    backend:
        Active backend identifier (e.g. ``"easyocr"``, ``"python_fallback"``).
    """

    availability: ServiceAvailability
    message: Optional[str] = field(default=None)
    backend: Optional[str] = field(default=None)

    @property
    def is_ok(self) -> bool:
        """Return True when the service is fully operational."""
        return self.availability == ServiceAvailability.AVAILABLE

    def as_dict(self) -> dict:
        return {
            "availability": self.availability.value,
            "message": self.message,
            "backend": self.backend,
        }


# ---------------------------------------------------------------------------
# Base Interface
# ---------------------------------------------------------------------------


class BaseAIService(ABC):
    """Shared contract for all CarePath AI services.

    Concrete engine classes must implement :meth:`health_check` and
    :meth:`get_service_info`.  These are used internally (not exposed over
    HTTP) to verify readiness and collect diagnostic metadata.
    """

    @abstractmethod
    def health_check(self) -> ServiceHealthStatus:
        """Return the current health status of this service.

        Must be cheap to call (no heavy inference).  May probe the
        underlying backend (e.g. ChromaDB ping) but must return within
        a few hundred milliseconds.
        """
        ...

    @abstractmethod
    def get_service_info(self) -> dict:
        """Return a dictionary of introspection metadata.

        At minimum the dict must include the keys:
        - ``"name"`` — human-readable service name
        - ``"version"`` — service version string
        - ``"status"`` — current :class:`ServiceAvailability` value

        Additional keys (backend, model_path, etc.) are encouraged.
        """
        ...


# ---------------------------------------------------------------------------
# Module-Specific Interfaces
# ---------------------------------------------------------------------------


class TextExtractionService(BaseAIService):
    """Interface for document OCR and text extraction engines.

    Implementations must support raw image/PDF bytes as input and return
    a structured ``OCRResult`` (``app.schemas.ocr.OCRResult``).
    """

    @abstractmethod
    def extract_text(self, image_bytes: bytes, filename: str = "document.png") -> object:
        """Extract structured text and medical data from document bytes.

        Parameters
        ----------
        image_bytes:
            Raw bytes of an image (PNG, JPEG, TIFF) or PDF document.
        filename:
            Original filename, used for format hinting and result metadata.

        Returns
        -------
        OCRResult
            Structured extraction result as defined in ``app.schemas.ocr``.
        """
        ...


class VisionAnalysisService(BaseAIService):
    """Interface for medical computer-vision and DICOM analysis engines.

    Implementations accept raw image or DICOM bytes and return a structured
    ``VisionAnalysisResult`` (``app.schemas.vision.VisionAnalysisResult``).
    """

    @abstractmethod
    def analyze_image(self, image_bytes: bytes, filename: str = "image.dcm") -> object:
        """Run diagnostic vision analysis on a medical image.

        Parameters
        ----------
        image_bytes:
            Raw bytes of a DICOM file or standard image format.
        filename:
            Original filename.  Used for DICOM detection hinting.

        Returns
        -------
        VisionAnalysisResult
            Structured analysis result as defined in ``app.schemas.vision``.
        """
        ...


class EntityExtractionService(BaseAIService):
    """Interface for clinical NLP and bio-NER engines.

    Implementations take unstructured clinical text and return a structured
    ``BioNERResult`` (``app.schemas.nlp.BioNERResult``).
    """

    @abstractmethod
    def extract_entities(self, text: str) -> object:
        """Extract medical entities, symptoms, medications, and ICD-10 codes.

        Parameters
        ----------
        text:
            Unstructured clinical text (notes, discharge summary, etc.).

        Returns
        -------
        BioNERResult
            Structured entity extraction result as defined in ``app.schemas.nlp``.
        """
        ...


class KnowledgeRetrievalService(BaseAIService):
    """Interface for medical knowledge RAG engines.

    Implementations query a vector database (or semantic keyword index)
    with a clinical question and return a ``RAGQueryResponse``
    (``app.schemas.rag.RAGQueryResponse``).
    """

    @abstractmethod
    def query_guidelines(self, query: str, top_k: int = 3) -> object:
        """Retrieve and synthesise relevant clinical guidelines.

        Parameters
        ----------
        query:
            Free-text clinical query (e.g. "management of community-acquired pneumonia").
        top_k:
            Maximum number of document chunks to retrieve.  Must be >= 1.

        Returns
        -------
        RAGQueryResponse
            Retrieval result as defined in ``app.schemas.rag``.
        """
        ...


class ClinicalSynthesisService(BaseAIService):
    """Interface for the multi-modal clinical synthesis engine.

    Implementations orchestrate OCR, Vision, NLP, and RAG modules to
    produce a ``PatientCarePathSynthesis``
    (``app.schemas.diagnosis.PatientCarePathSynthesis``).
    """

    @abstractmethod
    def synthesize_patient_case(
        self,
        clinical_notes: Optional[str] = None,
        document_bytes: Optional[bytes] = None,
        document_filename: str = "doc.png",
        image_bytes: Optional[bytes] = None,
        image_filename: str = "xray.png",
    ) -> object:
        """Synthesise multi-modal patient data into a structured CarePath report.

        Parameters
        ----------
        clinical_notes:
            Optional free-text clinical notes from the clinician.
        document_bytes:
            Optional raw bytes of a medical document (for OCR).
        document_filename:
            Original filename of the document.
        image_bytes:
            Optional raw bytes of a diagnostic image (for Vision).
        image_filename:
            Original filename of the image.

        Returns
        -------
        PatientCarePathSynthesis
            Full synthesis result as defined in ``app.schemas.diagnosis``.
        """
        ...
