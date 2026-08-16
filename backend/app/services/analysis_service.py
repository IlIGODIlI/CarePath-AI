from typing import Any, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.crud import ai_crud
from database.models import AIAnalysis
import uuid
from datetime import datetime, timezone

from database.crud.utils import safe_uuid

def start_analysis(session: Session, patient_id: str) -> AIAnalysis:
    now = datetime.now(timezone.utc)
    analysis_id = uuid.uuid4()
    uid = safe_uuid(patient_id)
    if not uid:
        raise ValueError(f"Invalid patient_id format: '{patient_id}'")
    # In a real scenario, this is where LangGraph orchestration starts.
    return ai_crud.create_analysis(
        session=session,
        analysis_id=analysis_id,
        user_id=uid,
        analysis_type="initial_triage",
        summary="Analysis started.",
        created_at=now,
        updated_at=now
    )

def get_analysis(session: Session, analysis_id: str) -> Optional[AIAnalysis]:
    from database.crud.utils import get_record
    aid = safe_uuid(analysis_id)
    if not aid:
        return None
    return get_record(session, AIAnalysis, aid)

def get_analysis_history(session: Session, patient_id: str) -> List[AIAnalysis]:
    uid = safe_uuid(patient_id)
    if not uid:
        return []
    return session.scalars(select(AIAnalysis).where(AIAnalysis.user_id == uid)).all()
