from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.connections import get_db
from app.services import patient_service
import uuid

router = APIRouter(prefix="/patients", tags=["Patients"])

class PatientData(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    # add other fields as necessary

@router.post("")
def create_patient(data: PatientData, db: Session = Depends(get_db)):
    try:
        profile = patient_service.create_patient(db, uuid.UUID(data.user_id), data.model_dump())
        db.commit()
        return profile
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("")
def get_all_patients(db: Session = Depends(get_db)):
    return patient_service.get_all_patients(db)

@router.get("/{patient_id}")
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    profile = patient_service.get_patient(db, uuid.UUID(patient_id))
    if not profile:
        raise HTTPException(status_code=404, detail="Patient not found")
    return profile

@router.put("/{patient_id}")
def update_patient(patient_id: str, data: dict, db: Session = Depends(get_db)):
    profile = patient_service.update_patient(db, uuid.UUID(patient_id), data)
    db.commit()
    return profile

@router.delete("/{patient_id}")
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    success = patient_service.delete_patient(db, uuid.UUID(patient_id))
    db.commit()
    return {"success": success}
