import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from src.agents.graph import carepath_graph, build_carepath_graph
from app.core.logging import logger


def run_carepath_agents(session_id: str, patient_id: str, raw_prompt: str, image_urls: list = None, doc_urls: list = None):
    initial_state = {
        "encounter_id": session_id,
        "patient_id": patient_id,
        "chief_complaint": raw_prompt,
        "attachments": [],
        "current_agent_id": "supervisor",
        "workflow_completed": False,
        "is_emergency": False,
        "emergency_alerts": [],
        "execution_history": [],
    }
    return carepath_graph.invoke(initial_state)


