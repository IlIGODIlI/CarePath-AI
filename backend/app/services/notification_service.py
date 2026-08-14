from typing import Any, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.crud import system_crud
from database.models import Notification
import uuid
from datetime import datetime, timezone

def get_notifications(session: Session) -> List[Notification]:
    # Mock for user "me" since we don't have proper JWT setup in this scope
    return session.scalars(select(Notification)).all()

def mark_notification_read(session: Session, notification_id: str) -> Notification:
    from database.crud.utils import update_record
    now = datetime.now(timezone.utc)
    return update_record(session, Notification, uuid.UUID(notification_id), is_read=True, read_at=now)
