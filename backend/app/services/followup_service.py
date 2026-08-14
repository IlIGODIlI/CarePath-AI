from typing import Any, List, Optional
from sqlalchemy.orm import Session
from database.crud import ai_crud
from database.models import FollowUp
import uuid
from datetime import datetime, timezone

def create_followup(session: Session, data: dict) -> FollowUp:
    now = datetime.now(timezone.utc)
    user_id = data.get("user_id")
    plan_id = data.get("plan_id")
    
    return ai_crud.create_followup(
        session=session,
        followup_id=uuid.uuid4(),
        user_id=uuid.UUID(user_id) if isinstance(user_id, str) else user_id,
        plan_id=uuid.UUID(plan_id) if isinstance(plan_id, str) and plan_id else None,
        followup_type=data.get("followup_type", "GENERAL"),
        scheduled_date=data.get("scheduled_date"),
        description=data.get("description", ""),
        purpose=data.get("purpose", ""),
        status=data.get("status", "SCHEDULED"),
        created_at=now,
        updated_at=now
    )

def get_followups(session: Session, patient_id: str, status: Optional[str] = None) -> List[FollowUp]:
    uid = uuid.UUID(patient_id) if isinstance(patient_id, str) else patient_id
    return ai_crud.get_user_followups(session=session, user_id=uid, status=status)

def complete_followup(session: Session, followup_id: str, notes: Optional[str] = None) -> Optional[FollowUp]:
    fid = uuid.UUID(followup_id) if isinstance(followup_id, str) else followup_id
    followup = ai_crud.update_followup_status(session, fid, status="COMPLETED", completed_date=datetime.now(timezone.utc))
    if followup and notes:
        from database.crud.utils import update_record
        return update_record(session, FollowUp, fid, notes=notes)
    return followup
