from typing import Any, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.crud import ai_crud
from database.models import FollowUp
import uuid
from datetime import datetime, timezone

def create_followup(session: Session, data: dict) -> FollowUp:
    now = datetime.now(timezone.utc)
    return ai_crud.create_followup(
        session=session,
        followup_id=uuid.uuid4(),
        user_id=uuid.UUID(data.get("user_id")),
        followup_type=data.get("followup_type", "GENERAL"),
        status="SCHEDULED",
        created_at=now,
        updated_at=now
    )

def get_followups(session: Session, patient_id: str) -> List[FollowUp]:
    return session.scalars(select(FollowUp).where(FollowUp.user_id == uuid.UUID(patient_id))).all()

def update_followup(session: Session, followup_id: str, data: dict) -> FollowUp:
    from database.crud.utils import update_record
    now = datetime.now(timezone.utc)
    data["updated_at"] = now
    return update_record(session, FollowUp, uuid.UUID(followup_id), **data)
