from typing import Any, List, Optional
from sqlalchemy.orm import Session
from database.crud import ai_crud
from database.models import CarePlan
import uuid
from datetime import datetime, timezone

def create_care_plan(session: Session, data: dict) -> CarePlan:
    now = datetime.now(timezone.utc)
    user_id = data.get("user_id")
    analysis_id = data.get("analysis_id")
    
    return ai_crud.create_care_plan(
        session=session,
        plan_id=uuid.uuid4(),
        user_id=uuid.UUID(user_id) if isinstance(user_id, str) else user_id,
        analysis_id=uuid.UUID(analysis_id) if isinstance(analysis_id, str) and analysis_id else None,
        plan_name=data.get("plan_name", "Personalized Care Plan"),
        plan_description=data.get("plan_description", ""),
        status=data.get("status", "ACTIVE"),
        next_steps=data.get("next_steps", ""),
        appointment_prep=data.get("appointment_prep", ""),
        lifestyle_changes=data.get("lifestyle_changes", ""),
        monitoring_points=data.get("monitoring_points", ""),
        estimated_duration=data.get("estimated_duration", ""),
        priority=data.get("priority", "MEDIUM"),
        created_at=now,
        updated_at=now
    )

def get_patient_care_plans(session: Session, patient_id: str, status: Optional[str] = None) -> List[CarePlan]:
    uid = uuid.UUID(patient_id) if isinstance(patient_id, str) else patient_id
    return ai_crud.get_user_care_plans(session=session, user_id=uid, status=status)

def update_care_plan_status(session: Session, plan_id: str, status: str) -> Optional[CarePlan]:
    pid = uuid.UUID(plan_id) if isinstance(plan_id, str) else plan_id
    return ai_crud.update_care_plan_status(session=session, plan_id=pid, status=status)
