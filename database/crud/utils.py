from typing import TypeVar, Type, Any, Optional
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")

def create_record(session: Session, model: Type[ModelType], **kwargs) -> ModelType:
    """
    Generic helper to create and commit a new record.
    Rolls back the session if an exception occurs.
    """
    try:
        obj = model(**kwargs)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj
    except Exception as e:
        session.rollback()
        raise e

def get_record(session: Session, model: Type[ModelType], record_id: Any) -> Optional[ModelType]:
    """
    Generic helper to retrieve a record by its primary key.
    """
    try:
        return session.get(model, record_id)
    except Exception as e:
        session.rollback()
        raise e

def update_record(session: Session, model: Type[ModelType], record_id: Any, **kwargs) -> Optional[ModelType]:
    """
    Generic helper to update a record.
    """
    try:
        obj = session.get(model, record_id)
        if not obj:
            return None
        for key, value in kwargs.items():
            setattr(obj, key, value)
        session.commit()
        session.refresh(obj)
        return obj
    except Exception as e:
        session.rollback()
        raise e

def delete_record(session: Session, model: Type[ModelType], record_id: Any) -> bool:
    """
    Generic helper to delete a record.
    """
    try:
        obj = session.get(model, record_id)
        if not obj:
            return False
        session.delete(obj)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
