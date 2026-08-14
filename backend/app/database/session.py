from typing import Generator
from database.connections import get_db, SessionLocal, engine, supabase
from database.models import Base


async def init_db():
    """Initializes database tables on application boot if needed."""
    if engine is not None:
        Base.metadata.create_all(bind=engine)

