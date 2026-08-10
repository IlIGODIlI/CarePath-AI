"""Clinical Bio-NER & Entity Extraction Subsystem."""
import re
import time
from typing import List
from app.schemas.nlp import BioNERResult, MedicalEntity
from app.core.logging import logger


class BioNEREngine:
    """Clinical Named Entity Recognition & Coding Engine."""

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

    def extract_entities(self, text: str) -> BioNERResult:
        """Extract medical entities, symptoms, medications, and ICD-10 codification."""
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
