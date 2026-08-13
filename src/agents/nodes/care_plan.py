from datetime import datetime
from typing import Dict, Any, List
from src.agents.state import CarePathState, UrgencyLevel
from src.core.logging import logger


async def care_plan_node(state: CarePathState) -> Dict[str, Any]:
    """LangGraph Node — Patient Care Plan Generator."""
    encounter_id = state.get("encounter_id", "unknown")
    logger.info("executing_care_plan_node", encounter_id=encounter_id)

    specialty = state.get("recommended_specialty") or "Specialist"
    urgency = state.get("urgency_level") or UrgencyLevel.ROUTINE
    is_emergency = state.get("is_emergency", False)

    if is_emergency or urgency == UrgencyLevel.EMERGENCY:
        action_items = [
            "CALL EMERGENCY SERVICES (911/112) IMMEDIATELY.",
            "Do not drive yourself to the hospital.",
            "Remain calm and keep patient still until emergency responders arrive.",
        ]
    else:
        action_items = [
            f"Schedule an appointment with a {specialty} provider within the recommended timeframe.",
            "Gather all past medical records, lab reports, and current medication lists.",
            "Track any changes in symptom severity using a daily log.",
        ]

    care_plan = {
        "action_items": action_items,
        "questions_for_doctor": [
            f"Based on my symptoms, do you suspect a specific condition related to {specialty}?",
            "What diagnostic tests do you recommend for my case?",
            "What warning signs should prompt me to seek emergency care?",
        ],
        "red_flag_warning_signs": [
            "Sudden severe spike in fever (>102°F / 38.9°C).",
            "Inability to keep fluids down due to persistent vomiting.",
            "Sudden onset of unbearable pain, dizziness, or fainting.",
        ],
        "home_care_guidance": (
            "Maintain rest and stay hydrated. Avoid unprescribed pain relievers that may mask pain signals."
        ),
    }

    execution_history = state.get("execution_history", [])
    execution_history.append({
        "step_id": f"step_care_plan_{len(execution_history)}",
        "agent_name": "CarePlanAgent",
        "started_at": datetime.utcnow().isoformat(),
        "completed_at": datetime.utcnow().isoformat(),
        "status": "SUCCESS",
        "state_delta_keys": ["patient_care_plan"],
        "error_message": None,
    })

    return {
        "patient_care_plan": care_plan["action_items"],
        "execution_history": execution_history,
    }
