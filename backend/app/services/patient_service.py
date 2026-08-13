from typing import Any, Optional, List
from sqlalchemy.orm import Session
from database.crud import user_crud
from database.models import PatientProfile
import uuid
from datetime import datetime, timezone

def create_patient(session: Session, user_id: Any, data: dict) -> PatientProfile:
    now = datetime.now(timezone.utc)
    # Check if user exists
    user = user_crud.get_user(session, user_id)
    if not user:
        raise ValueError("User not found")
        
    return user_crud.create_patient_profile(
        session=session,
        user_id=user_id,
        first_name=data.get("first_name", ""),
        last_name=data.get("last_name", ""),
        created_at=now,
        updated_at=now
    )

def get_patient(session: Session, user_id: Any) -> Optional[PatientProfile]:
    return user_crud.get_patient_profile(session, user_id)

def update_patient(session: Session, user_id: Any, data: dict) -> Optional[PatientProfile]:
    # user_crud doesn't have update_patient_profile, we will update user_crud later or use generic update
    from database.crud.utils import update_record
    now = datetime.now(timezone.utc)
    data["updated_at"] = now
    return update_record(session, PatientProfile, user_id, **data)

def delete_patient(session: Session, user_id: Any) -> bool:
    from database.crud.utils import delete_record
    return delete_record(session, PatientProfile, user_id)

def get_all_patients(session: Session) -> List[PatientProfile]:
    from sqlalchemy import select
    return session.scalars(select(PatientProfile)).all()
