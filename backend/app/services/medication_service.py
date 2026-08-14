from typing import Any, List, Optional
from sqlalchemy.orm import Session
from database.crud import clinical_crud
from database.models import Medication
import uuid
from datetime import datetime, timezone

def add_medication(session: Session, data: dict) -> Medication:
    now = datetime.now(timezone.utc)
    user_id = data.get("user_id")
    
    return clinical_crud.create_medication(
        session=session,
        medication_id=uuid.uuid4(),
        user_id=uuid.UUID(user_id) if isinstance(user_id, str) else user_id,
        medication_name=data.get("medication_name", ""),
        dosage=data.get("dosage", ""),
        frequency=data.get("frequency", ""),
        duration=data.get("duration", ""),
        route=data.get("route", "oral"),
        start_date=data.get("start_date"),
        end_date=data.get("end_date"),
        purpose=data.get("purpose", ""),
        side_effects=data.get("side_effects", ""),
        instructions=data.get("instructions", ""),
        prescribed_by=data.get("prescribed_by", ""),
        status=data.get("status", "ACTIVE"),
        created_at=now,
        updated_at=now
    )

def get_patient_medications(session: Session, patient_id: str, status: Optional[str] = None) -> List[Medication]:
    uid = uuid.UUID(patient_id) if isinstance(patient_id, str) else patient_id
    return clinical_crud.get_user_medications(session=session, user_id=uid, status=status)

def update_medication_status(session: Session, medication_id: str, status: str) -> Optional[Medication]:
    mid = uuid.UUID(medication_id) if isinstance(medication_id, str) else medication_id
    return clinical_crud.update_medication_status(session=session, medication_id=mid, status=status)
