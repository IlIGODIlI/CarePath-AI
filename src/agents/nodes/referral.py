from datetime import datetime
from typing import Dict, Any, List, Optional
from src.agents.state import CarePathState, UrgencyLevel
from src.config import settings
from src.core.logging import logger


async def referral_node(state: CarePathState) -> Dict[str, Any]:
    """
    LangGraph Node Wrapper for Referral Agent.
    """
    encounter_id = state.get("encounter_id", "unknown")
    logger.info("executing_referral_node", encounter_id=encounter_id)

    hypotheses = state.get("clinical_hypotheses", [])
    urgency = state.get("urgency_level") or UrgencyLevel.ROUTINE

    primary_specialty = "General Internal Medicine"
    if hypotheses and "Appendicitis" in hypotheses[0].get("condition_name", ""):
        primary_specialty = "General Surgery"
        urgency = UrgencyLevel.URGENT

    execution_history = state.get("execution_history", [])
    execution_history.append({
        "step_id": f"step_referral_{len(execution_history)}",
        "agent_name": "ReferralAgent",
        "started_at": datetime.utcnow().isoformat(),
        "completed_at": datetime.utcnow().isoformat(),
        "status": "SUCCESS",
        "state_delta_keys": ["recommended_specialty", "urgency_level"],
        "error_message": None,
    })

    return {
        "recommended_specialty": primary_specialty,
        "urgency_level": urgency,
        "execution_history": execution_history,
    }
