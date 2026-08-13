from typing import Any
from sqlalchemy.orm import Session
from database.storage import upload_file
import uuid
from datetime import datetime, timezone

def handle_upload(session: Session, file_path: str, user_id: str, file_type: str) -> dict:
    dest = f"uploads/{user_id}/{uuid.uuid4()}_{file_type}"
    try:
        return upload_file(file_path, dest)
    except Exception as e:
        return {"error": str(e)}
