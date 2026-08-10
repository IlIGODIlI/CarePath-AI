"""Clinical NLP and Bio-NER Schemas."""
from typing import List, Optional
from pydantic import BaseModel, Field


class MedicalEntity(BaseModel):
    text: str
    category: str = Field(description="SYMPTOM, MEDICATION, ANATOMY, PROCEDURE, DIAGNOSIS, LAB_METRIC")
    icd10_code: Optional[str] = None
    snomed_ct: Optional[str] = None
    negated: bool = False
    confidence: float = 0.90


class BioNERResult(BaseModel):
    input_text: str
    entities: List[MedicalEntity] = Field(default_factory=list)
    symptoms: List[str] = Field(default_factory=list)
    medications: List[str] = Field(default_factory=list)
    diagnoses: List[str] = Field(default_factory=list)
    processing_time_seconds: float
