"""OCR Data Schemas and Response DTOs."""
from typing import List, Optional
from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x_min: int
    y_min: int
    x_max: int
    y_max: int


class ExtractedTextLine(BaseModel):
    text: str
    confidence: float
    bbox: Optional[BoundingBox] = None


class LabMetricItem(BaseModel):
    test_name: str
    value: str
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    status: Optional[str] = None  # e.g., NORMAL, HIGH, LOW


class PrescriptionItem(BaseModel):
    drug_name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None


class OCRResult(BaseModel):
    filename: str
    document_type: str = Field(description="e.g. PRESCRIPTION, LAB_REPORT, CLINICAL_NOTE, GENERAL")
    raw_text: str
    confidence_score: float
    page_count: int = 1
    lab_metrics: List[LabMetricItem] = Field(default_factory=list)
    prescriptions: List[PrescriptionItem] = Field(default_factory=list)
    text_lines: List[ExtractedTextLine] = Field(default_factory=list)
    processing_time_seconds: float
