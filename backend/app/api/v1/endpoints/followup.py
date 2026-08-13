from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.connections import get_db
from app.services import followup_service

router = APIRouter(prefix="/followup", tags=["FollowUp"])

class FollowUpData(BaseModel):
    user_id: str
    followup_type: str

@router.post("")
def create_followup(data: FollowUpData, db: Session = Depends(get_db)):
    fup = followup_service.create_followup(db, data.model_dump())
    db.commit()
    return fup

@router.get("/{patient_id}")
def get_followups(patient_id: str, db: Session = Depends(get_db)):
    return followup_service.get_followups(db, patient_id)

@router.put("/{followup_id}")
def update_followup(followup_id: str, data: dict, db: Session = Depends(get_db)):
    fup = followup_service.update_followup(db, followup_id, data)
    db.commit()
    return fup
