from typing import Any, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.crud import ai_crud
from database.models import AIAnalysis
import uuid
from datetime import datetime, timezone

def start_analysis(session: Session, patient_id: str) -> AIAnalysis:
    now = datetime.now(timezone.utc)
    analysis_id = uuid.uuid4()
    # In a real scenario, this is where LangGraph orchestration starts.
    return ai_crud.create_analysis(
        session=session,
        analysis_id=analysis_id,
        user_id=uuid.UUID(patient_id),
        analysis_type="initial_triage",
        summary="Analysis started.",
        created_at=now,
        updated_at=now
    )

def get_analysis(session: Session, analysis_id: str) -> Optional[AIAnalysis]:
    from database.crud.utils import get_record
    return get_record(session, AIAnalysis, uuid.UUID(analysis_id))

def get_analysis_history(session: Session, patient_id: str) -> List[AIAnalysis]:
    return session.scalars(select(AIAnalysis).where(AIAnalysis.user_id == uuid.UUID(patient_id))).all()
