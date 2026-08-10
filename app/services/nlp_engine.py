"""Clinical Bio-NER & Entity Extraction Subsystem."""
import re
import time
from typing import List
from app.schemas.nlp import BioNERResult, MedicalEntity
from app.core.logging import get_logger
from app.core.interfaces import EntityExtractionService, ServiceHealthStatus, ServiceAvailability
from app.core.validation import validate_text_input
from app.core.config import settings

logger = get_logger(__name__)


class BioNEREngine(EntityExtractionService):
    """Clinical Named Entity Recognition & Coding Engine."""

    _SERVICE_NAME = "CarePath Bio-NER Engine"
    _SERVICE_VERSION = "0.1.0"

    # Medical terminology dictionaries with ICD-10 codification
    ICD10_MAP = {
        "pneumonia": ("DIAGNOSIS", "J18.9"),
        "fever": ("SYMPTOM", "R50.9"),
        "cough": ("SYMPTOM", "R05"),
        "dyspnea": ("SYMPTOM", "R06.0"),
        "shortness of breath": ("SYMPTOM", "R06.0"),
        "chest pain": ("SYMPTOM", "R07.9"),
        "diabetes": ("DIAGNOSIS", "E11.9"),
        "hypertension": ("DIAGNOSIS", "I10"),
        "amoxicillin": ("MEDICATION", "ATC:J01CA04"),
        "metformin": ("MEDICATION", "ATC:A10BA02"),
        "paracetamol": ("MEDICATION", "ATC:N02BE01"),
        "acetaminophen": ("MEDICATION", "ATC:N02BE01"),
        "lung": ("ANATOMY", "SNOMED:39607008"),
        "chest": ("ANATOMY", "SNOMED:51185008")
    }

    def __init__(self):
        logger.info("Bio-NER Engine initialized.")

    # ------------------------------------------------------------------
    # Interface: BaseAIService
    # ------------------------------------------------------------------

    def health_check(self) -> ServiceHealthStatus:
        """Return health status — always AVAILABLE (pure Python, no external deps)."""
        return ServiceHealthStatus(
            availability=ServiceAvailability.AVAILABLE,
            backend="regex_icd10_map",
            message="Bio-NER regex/ICD-10 engine is active.",
        )

    def get_service_info(self) -> dict:
        """Return metadata about this NLP engine instance."""
        return {
            "name": self._SERVICE_NAME,
            "version": self._SERVICE_VERSION,
            "status": ServiceAvailability.AVAILABLE.value,
            "backend": "regex_icd10_map",
            "entity_count": len(self.ICD10_MAP),
            "confidence_threshold": settings.NLP_CONFIDENCE_THRESHOLD,
        }

    def extract_entities(self, text: str) -> BioNERResult:
        """Extract medical entities, symptoms, medications, and ICD-10 codification."""
        validate_text_input(text, min_len=1, max_len=32_768)
        start_time = time.time()
        entities: List[MedicalEntity] = []
        symptoms: List[str] = []
        medications: List[str] = []
        diagnoses: List[str] = []

        text_lower = text.lower()

        # Negation check phrases
        negation_patterns = [r"no\s+", r"denies\s+", r"without\s+", r"absent\s+"]

        for term, (category, code) in self.ICD10_MAP.items():
            pattern = r"\b" + re.escape(term) + r"\b"
            for match in re.finditer(pattern, text_lower):
                # Check for negation in 30 characters preceding match
                start_pos = max(0, match.start() - 30)
                prefix = text_lower[start_pos:match.start()]
                is_negated = any(re.search(neg, prefix) for neg in negation_patterns)

                match_text = text[match.start():match.end()]

                entity = MedicalEntity(
                    text=match_text,
                    category=category,
                    icd10_code=code,
                    negated=is_negated,
                    confidence=0.95
                )
                entities.append(entity)

                if not is_negated:
                    if category == "SYMPTOM" and match_text not in symptoms:
                        symptoms.append(match_text)
                    elif category == "MEDICATION" and match_text not in medications:
                        medications.append(match_text)
                    elif category == "DIAGNOSIS" and match_text not in diagnoses:
                        diagnoses.append(match_text)

        elapsed = round(time.time() - start_time, 3)

        return BioNERResult(
            input_text=text,
            entities=entities,
            symptoms=symptoms,
            medications=medications,
            diagnoses=diagnoses,
            processing_time_seconds=elapsed
        )


nlp_engine = BioNEREngine()
