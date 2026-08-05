"""
CarePath AI - Global Shared Graph State Definition
=================================================
Defines the `CarePathGlobalState` TypedDict used by LangGraph to pass immutable
state snapshots across all 11 autonomous agents.

Includes custom reducers for append-only audit histories, state deltas, and emergency flags.
"""

from typing import Annotated, Any, Dict, List, Optional, TypedDict
from pydantic import BaseModel, Field


# --- Pydantic Sub-Models for Structured Agent Outputs ---

class StructuredSymptom(BaseModel):
    chief_complaint: str
    symptom_list: List[str] = Field(default_factory=list)
    duration: Optional[str] = None
    severity_score: int = Field(default=5, ge=1, le=10)
    aggravating_factors: List[str] = Field(default_factory=list)
    relieving_factors: List[str] = Field(default_factory=list)
    body_locations: List[str] = Field(default_factory=list)


class VisionFinding(BaseModel):
    anatomical_region: str
    visual_observations: List[str]
    lesion_type: Optional[str] = None
    image_quality_score: float = Field(default=1.0, ge=0.0, le=1.0)
    flagged_for_review: bool = False


class ParsedMedicalDoc(BaseModel):
    document_type: str  # LAB_REPORT, PRESCRIPTION, DISCHARGE_SUMMARY
    lab_results: Dict[str, Any] = Field(default_factory=dict)
    abnormal_flags: List[str] = Field(default_factory=list)
    icd10_codes: List[str] = Field(default_factory=list)
    prescriptions: List[Dict[str, str]] = Field(default_factory=list)


class ClinicalTimelineEvent(BaseModel):
    event_date: Optional[str] = None
    category: str  # SYMPTOM_ONSET, LAB_TEST, SURGERY, MEDICATION
    title: str
    details: str


class RetrievedEvidence(BaseModel):
    source_title: str
    guideline_body: str
    relevance_score: float
    citation: str
    specialty_match: str


class DifferentialSpecialty(BaseModel):
    specialty_name: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    clinical_rationale: str
    supporting_evidence_ids: List[str] = Field(default_factory=list)


class SpecialistReferral(BaseModel):
    primary_specialty: str
    secondary_specialty: Optional[str] = None
    triage_urgency: str  # EMERGENCY_911, URGENT_48HRS, SPECIALIST_EVALUATION, ROUTINE
    doctor_questions: List[str] = Field(default_factory=list)
    recommended_timeframe: str


class PatientCarePlan(BaseModel):
    action_items: List[str]
    symptom_tracking_guide: List[str]
    preparation_checklist: List[str]
    plain_language_summary: str


class ExecutionStepLog(BaseModel):
    step_number: int
    agent_id: str
    agent_name: str
    status: str  # SUCCESS, FAILED, EMERGENCY_TRIGGERED, SKIPPED
    decision: str
    execution_time_ms: float
    confidence_score: float
    timestamp_iso: str


# --- Custom Reducer Functions for LangGraph State ---

def append_logs(existing: List[Dict[str, Any]], new_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Reducer that appends execution logs immutably."""
    return existing + new_items


def append_alerts(existing: List[str], new_items: List[str]) -> List[str]:
    """Reducer that appends emergency alert strings."""
    return list(set(existing + new_items))


# --- LangGraph Shared State Schema ---

class CarePathGlobalState(TypedDict):
    """
    CarePathGlobalState represents the single source of truth across the entire
    11-agent LangGraph execution graph.
    """
    # Session & Patient Metadata
    session_id: str
    patient_id: str
    created_at_iso: str

    # User Input Artifacts
    raw_prompt: str
    uploaded_image_urls: List[str]
    uploaded_doc_urls: List[str]

    # Agent Output Artifacts (Populated dynamically)
    structured_symptoms: Optional[StructuredSymptom]
    vision_findings: Optional[VisionFinding]
    parsed_docs: Optional[ParsedMedicalDoc]
    clinical_timeline: List[ClinicalTimelineEvent]
    retrieved_evidence: List[RetrievedEvidence]
    differential_specialties: List[DifferentialSpecialty]
    referral_recommendation: Optional[SpecialistReferral]
    care_plan: Optional[PatientCarePlan]
    followup_scheduled: Optional[Dict[str, Any]]

    # Workflow Controls & Safety Overrides
    is_emergency: bool
    emergency_alerts: Annotated[List[str], append_alerts]
    missing_information: List[str]
    workflow_completed: bool
    current_agent_id: str
    overall_confidence: float

    # Audit Trail & Execution Memory
    execution_history: Annotated[List[Dict[str, Any]], append_logs]
    retry_counts: Dict[str, int]
