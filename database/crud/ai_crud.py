from sqlalchemy.orm import Session
from database.models import AIAnalysis, Recommendation, CarePlan, FollowUp
from database.crud.utils import create_record

def create_analysis(session: Session, **kwargs) -> AIAnalysis:
    """Creates a new AI analysis record."""
    return create_record(session, AIAnalysis, **kwargs)

def create_recommendation(session: Session, **kwargs) -> Recommendation:
    """Creates a new recommendation linked to an analysis."""
    return create_record(session, Recommendation, **kwargs)

def create_care_plan(session: Session, **kwargs) -> CarePlan:
    """Creates a new care plan."""
    return create_record(session, CarePlan, **kwargs)

def create_followup(session: Session, **kwargs) -> FollowUp:
    """Creates a new follow-up appointment or task."""
    return create_record(session, FollowUp, **kwargs)
