"""
CarePath AI - LangGraph Workflow Graph Assembly
==============================================
Assembles the compiled 11-agent StateGraph with conditional routing, parallel worker edges,
safety bypasses, and state execution history.
"""

from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, END

from app.agents.state import CarePathGlobalState
from app.agents.nodes import (
    supervisor_node,
    safety_node,
    intake_node,
    vision_node,
    docs_node,
    timeline_node,
    evidence_node,
    clinical_reasoning_node,
    referral_node,
    care_plan_node,
    followup_node,
)


def router_conditional_edge(state: CarePathGlobalState) -> str:
    """
    Evaluates global state and returns the next node key for LangGraph conditional branching.
    """
    if state.get("is_emergency"):
        return "SAFETY"
    
    # Check execution history for latest supervisor node log or inspect state fields directly
    if not state.get("structured_symptoms"):
        return "INTAKE"
    
    if state.get("uploaded_image_urls") and not state.get("vision_findings"):
        return "VISION"
    
    if state.get("uploaded_doc_urls") and not state.get("parsed_docs"):
        return "DOCS"
    
    if not state.get("clinical_timeline"):
        return "TIMELINE"
    
    if not state.get("retrieved_evidence"):
        return "EVIDENCE"
    
    if not state.get("differential_specialties"):
        return "CLINICAL_REASONING"
    
    if not state.get("referral_recommendation"):
        return "REFERRAL"
    
    if not state.get("care_plan"):
        return "CARE_PLAN"
    
    if not state.get("followup_scheduled"):
        return "FOLLOW_UP"
    
    return "END"


def build_carepath_graph():
    """
    Constructs and compiles the full CarePath AI multi-agent graph.
    """
    workflow = StateGraph(CarePathGlobalState)

    # 1. Add All 11 Agent Nodes
    workflow.add_node("SUPERVISOR", supervisor_node)
    workflow.add_node("SAFETY", safety_node)
    workflow.add_node("INTAKE", intake_node)
    workflow.add_node("VISION", vision_node)
    workflow.add_node("DOCS", docs_node)
    workflow.add_node("TIMELINE", timeline_node)
    workflow.add_node("EVIDENCE", evidence_node)
    workflow.add_node("CLINICAL_REASONING", clinical_reasoning_node)
    workflow.add_node("REFERRAL", referral_node)
    workflow.add_node("CARE_PLAN", care_plan_node)
    workflow.add_node("FOLLOW_UP", followup_node)

    # 2. Set Entry Point to Safety Agent First
    workflow.set_entry_point("SAFETY")

    # 3. From Safety -> Route to Supervisor if safe, or END if emergency
    workflow.add_conditional_edges(
        "SAFETY",
        lambda state: "END" if state.get("is_emergency") else "SUPERVISOR",
        {
            "END": END,
            "SUPERVISOR": "SUPERVISOR"
        }
    )

    # 4. Supervisor dynamic routing edges
    workflow.add_conditional_edges(
        "SUPERVISOR",
        router_conditional_edge,
        {
            "SAFETY": "SAFETY",
            "INTAKE": "INTAKE",
            "VISION": "VISION",
            "DOCS": "DOCS",
            "TIMELINE": "TIMELINE",
            "EVIDENCE": "EVIDENCE",
            "CLINICAL_REASONING": "CLINICAL_REASONING",
            "REFERRAL": "REFERRAL",
            "CARE_PLAN": "CARE_PLAN",
            "FOLLOW_UP": "FOLLOW_UP",
            "END": END
        }
    )

    # 5. Worker Nodes return back to Supervisor
    worker_nodes = [
        "INTAKE", "VISION", "DOCS", "TIMELINE", "EVIDENCE",
        "CLINICAL_REASONING", "REFERRAL", "CARE_PLAN", "FOLLOW_UP"
    ]
    for w_node in worker_nodes:
        workflow.add_edge(w_node, "SUPERVISOR")

    # Compile Graph
    compiled_app = workflow.compile()
    return compiled_app


# Singleton compiled graph app instance
carepath_graph_app = build_carepath_graph()


def run_carepath_agents(
    session_id: str,
    patient_id: str,
    raw_prompt: str,
    image_urls: list = None,
    doc_urls: list = None
) -> CarePathGlobalState:
    """
    Executes the compiled multi-agent graph with initial state parameters.
    """
    initial_state: CarePathGlobalState = {
        "session_id": session_id,
        "patient_id": patient_id,
        "created_at_iso": "",
        "raw_prompt": raw_prompt,
        "uploaded_image_urls": image_urls or [],
        "uploaded_doc_urls": doc_urls or [],
        "structured_symptoms": None,
        "vision_findings": None,
        "parsed_docs": None,
        "clinical_timeline": [],
        "retrieved_evidence": [],
        "differential_specialties": [],
        "referral_recommendation": None,
        "care_plan": None,
        "followup_scheduled": None,
        "is_emergency": False,
        "emergency_alerts": [],
        "missing_information": [],
        "workflow_completed": False,
        "current_agent_id": "INIT",
        "overall_confidence": 0.0,
        "execution_history": [],
        "retry_counts": {}
    }

    final_state = carepath_graph_app.invoke(initial_state)
    return final_state
