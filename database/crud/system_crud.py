from sqlalchemy.orm import Session
from database.models import Notification, Feedback, AgentRun, TimelineEvent, EvidenceRetrieval
from database.crud.utils import create_record

def create_notification(session: Session, **kwargs) -> Notification:
    """Creates a system notification for a user."""
    return create_record(session, Notification, **kwargs)

def create_feedback(session: Session, **kwargs) -> Feedback:
    """Records user feedback."""
    return create_record(session, Feedback, **kwargs)

def create_agent_run(session: Session, **kwargs) -> AgentRun:
    """Logs the execution details of an AI agent."""
    return create_record(session, AgentRun, **kwargs)

def create_timeline_event(session: Session, **kwargs) -> TimelineEvent:
    """Creates an event on the patient's timeline."""
    return create_record(session, TimelineEvent, **kwargs)

def create_evidence(session: Session, **kwargs) -> EvidenceRetrieval:
    """Logs retrieved evidence used in agent reasoning."""
    return create_record(session, EvidenceRetrieval, **kwargs)
