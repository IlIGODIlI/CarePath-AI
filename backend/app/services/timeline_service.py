from typing import Any, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.crud import clinical_crud
from database.models import TimelineEvent
import uuid
from datetime import datetime, timezone

def get_timeline_events(session: Session, patient_id: str) -> List[TimelineEvent]:
    return session.scalars(select(TimelineEvent).where(TimelineEvent.user_id == uuid.UUID(patient_id))).all()

def add_timeline_event(session: Session, data: dict) -> TimelineEvent:
    now = datetime.now(timezone.utc)
    return clinical_crud.create_timeline_event(
        session=session,
        event_id=uuid.uuid4(),
        user_id=uuid.UUID(data.get("user_id")),
        event_type=data.get("event_type", "GENERAL"),
        event_title=data.get("event_title", ""),
        created_at=now
    )
