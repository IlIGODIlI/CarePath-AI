"""
CarePath AI - Agent Orchestration Endpoints
===========================================
Exposes REST endpoints to trigger the 11-agent LangGraph workflow, retrieve graph state,
and inspect agent specifications.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from app.agents.graph import run_carepath_agents
from app.agents.specs import AGENT_SPECIFICATIONS
from app.core.logging import logger

router = APIRouter(prefix="/agents", tags=["Agent Orchestration"])


class OrchestrationRequest(BaseModel):
    session_id: str = Field(..., example="sess_9921_x82")
    patient_id: str = Field(..., example="pat_1028_u01")
    raw_prompt: str = Field(..., example="I have a red rash on my leg for 3 days and my fever is 101F")
    uploaded_image_urls: List[str] = Field(default_factory=list)
    uploaded_doc_urls: List[str] = Field(default_factory=list)


class OrchestrationResponse(BaseModel):
    session_id: str
    patient_id: str
    is_emergency: bool
    emergency_alerts: List[str]
    workflow_completed: bool
    overall_confidence: float
    current_agent_id: str
    execution_history: List[Dict[str, Any]]
    structured_symptoms: Optional[Dict[str, Any]] = None
    vision_findings: Optional[Dict[str, Any]] = None
    parsed_docs: Optional[Dict[str, Any]] = None
    clinical_timeline: List[Dict[str, Any]] = Field(default_factory=list)
    retrieved_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    differential_specialties: List[Dict[str, Any]] = Field(default_factory=list)
    referral_recommendation: Optional[Dict[str, Any]] = None
    care_plan: Optional[Dict[str, Any]] = None
    followup_scheduled: Optional[Dict[str, Any]] = None


@router.post("/orchestrate", response_model=OrchestrationResponse)
async def orchestrate_agents(payload: OrchestrationRequest):
    """
    Triggers the autonomous 11-agent LangGraph orchestration pipeline.
    """
    logger.info("Starting Multi-Agent Orchestration", session_id=payload.session_id, prompt=payload.raw_prompt[:60])
    try:
        final_state = run_carepath_agents(
            session_id=payload.session_id,
            patient_id=payload.patient_id,
            raw_prompt=payload.raw_prompt,
            image_urls=payload.uploaded_image_urls,
            doc_urls=payload.uploaded_doc_urls
        )

        # Helper to convert pydantic/dataclass models to dict if necessary
        def to_dict(obj):
            if hasattr(obj, "dict"):
                return obj.dict()
            elif hasattr(obj, "model_dump"):
                return obj.model_dump()
            return obj

        return OrchestrationResponse(
            session_id=final_state.get("session_id"),
            patient_id=final_state.get("patient_id"),
            is_emergency=final_state.get("is_emergency", False),
            emergency_alerts=final_state.get("emergency_alerts", []),
            workflow_completed=final_state.get("workflow_completed", False),
            overall_confidence=final_state.get("overall_confidence", 0.0),
            current_agent_id=final_state.get("current_agent_id", "DONE"),
            execution_history=final_state.get("execution_history", []),
            structured_symptoms=to_dict(final_state.get("structured_symptoms")),
            vision_findings=to_dict(final_state.get("vision_findings")),
            parsed_docs=to_dict(final_state.get("parsed_docs")),
            clinical_timeline=[to_dict(item) for item in final_state.get("clinical_timeline", [])],
            retrieved_evidence=[to_dict(item) for item in final_state.get("retrieved_evidence", [])],
            differential_specialties=[to_dict(item) for item in final_state.get("differential_specialties", [])],
            referral_recommendation=to_dict(final_state.get("referral_recommendation")),
            care_plan=to_dict(final_state.get("care_plan")),
            followup_scheduled=to_dict(final_state.get("followup_scheduled"))
        )
    except Exception as e:
        logger.error("Multi-Agent Orchestration Failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Agent workflow error: {str(e)}")


@router.get("/specs")
async def get_agent_specs():
    """
    Returns the complete registry specification for all 11 agents in CarePath AI.
    """
    return {
        "agent_count": len(AGENT_SPECIFICATIONS),
        "agents": AGENT_SPECIFICATIONS
    }
