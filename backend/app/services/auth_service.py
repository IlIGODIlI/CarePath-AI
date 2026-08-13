from typing import Any, Optional
from sqlalchemy.orm import Session
from database.crud import user_crud
from database.models import User
import uuid
from datetime import datetime, timezone

def register_user(session: Session, email: str, password_hash: str) -> User:
    # In a real app, hash the password here
    user_id = uuid.uuid4()
    now = datetime.now(timezone.utc)
    return user_crud.create_user(
        session=session,
        user_id=user_id,
        email=email,
        password_hash=password_hash,
        role="patient",
        account_status="active",
        created_at=now,
        updated_at=now
    )

def authenticate_user(session: Session, email: str, password_hash: str) -> Optional[User]:
    user = user_crud.get_user_by_email(session, email)
    if user and user.password_hash == password_hash:
        return user
    return None

def get_user_profile(session: Session, user_id: Any) -> Optional[User]:
    return user_crud.get_user(session, user_id)
