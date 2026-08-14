from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connections import get_db
from app.services import notification_service

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("")
def get_notifications(db: Session = Depends(get_db)):
    return notification_service.get_notifications(db)

@router.put("/{notification_id}/read")
def mark_read(notification_id: str, db: Session = Depends(get_db)):
    notif = notification_service.mark_notification_read(db, notification_id)
    db.commit()
    return notif
