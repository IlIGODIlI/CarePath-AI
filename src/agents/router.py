from src.agents.state import CarePathState, UrgencyLevel
from src.core.logging import logger

# Emergency keywords for fast pre-check before routing to Safety node
_EMERGENCY_KEYWORDS = [
    "crushing chest pain", "chest pain", "shortness of breath",
    "sudden weakness", "face drooping", "slurred speech",
    "anaphylaxis", "throat closing", "unconscious", "unresponsive",
    "coughing blood", "vomiting blood", "suicidal", "stroke",
    "heart attack", "cardiac arrest",
]


def _has_emergency_keywords(complaint: str) -> bool:
    """Fast O(n) scan for emergency keywords — no regex overhead."""
    text = complaint.lower()
    return any(kw in text for kw in _EMERGENCY_KEYWORDS)


def supervisor_router(state: CarePathState) -> str:
    """
    Dynamic Supervisor Router.
    Evaluates CarePathState invariants to determine the next agent node.
    Safety check is the FIRST gate — always before any other routing.
    """
    logger.info(
        "supervisor_evaluating_state",
        encounter_id=state.get("encounter_id"),
        is_emergency=state.get("is_emergency"),
        confidence=state.get("confidence_score", 0.0),
    )

    # ── 1. Safety gate — HIGHEST PRIORITY ───────────────────────────────────
    # If confirmed emergency:
    # - If care plan already populated → terminate
    # - Otherwise → route to safety to populate emergency care plan
    if state.get("is_emergency"):
        if state.get("patient_care_plan"):
            return "__end__"
        return "safety"

    # If symptoms look like an emergency but Safety hasn't confirmed yet → run Safety
    complaint = state.get("chief_complaint", "")
    severity  = state.get("symptoms_severity") or 0
    if _has_emergency_keywords(complaint) or severity >= 9:
        if not state.get("emergency_reasoning"):
            return "safety"

    # ── 2. Intake normalization ──────────────────────────────────────────────
    if not state.get("structured_symptoms"):
        return "intake"

    # ── 3. Perception phase ──────────────────────────────────────────────────
    attachments = state.get("attachments", [])
    if any(a.get("file_type") == "IMAGE"     and not a.get("processed") for a in attachments):
        return "vision"
    if any(a.get("file_type") == "DOCUMENT"  and not a.get("processed") for a in attachments):
        return "docs"

    # ── 4. Reasoning pipeline ────────────────────────────────────────────────
    if not state.get("patient_timeline"):
        return "timeline"
    if not state.get("rag_evidence_docs"):
        return "evidence"
    if not state.get("clinical_hypotheses"):
        return "clinical_reasoning"

    # ── 5. Low-confidence clarification loop ────────────────────────────────
    if state.get("confidence_score", 1.0) < 0.60 and state.get("needs_more_info"):
        logger.info("low_confidence_requesting_more_info",
                    encounter_id=state.get("encounter_id"))
        return "__end__"

    # ── 6. Action phase ──────────────────────────────────────────────────────
    if not state.get("recommended_specialty"):
        return "referral"
    if not state.get("patient_care_plan"):
        return "care_plan"
    if not state.get("follow_up_schedule"):
        return "follow_up"

    return "__end__"
