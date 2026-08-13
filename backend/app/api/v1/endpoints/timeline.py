from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.connections import get_db
from app.services import timeline_service

router = APIRouter(prefix="/timeline", tags=["Timeline"])

class TimelineEventData(BaseModel):
    user_id: str
    event_type: str
    event_title: str

@router.get("/{patient_id}")
def get_timeline(patient_id: str, db: Session = Depends(get_db)):
    return timeline_service.get_timeline_events(db, patient_id)

@router.post("/event")
def add_event(data: TimelineEventData, db: Session = Depends(get_db)):
    event = timeline_service.add_timeline_event(db, data.model_dump())
    db.commit()
    return event
