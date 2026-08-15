import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from supabase import create_client, Client
from dotenv import load_dotenv, find_dotenv

# Base class for SQLAlchemy models
Base = declarative_base()

# Load environment variables from .env file (auto-searches parent directories)
load_dotenv(find_dotenv(usecwd=True))


# --- PostgreSQL Connection (via SQLAlchemy) ---
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Supabase sometimes provides PostgreSQL URLs starting with postgres:// 
    # SQLAlchemy 1.4+ requires postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    if "+asyncpg" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("+asyncpg", "", 1)

        
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    print("WARNING: DATABASE_URL not found in environment variables.")
    engine = None
    SessionLocal = None

def get_db():
    """Dependency to get a database session (useful for FastAPI etc.)"""
    if SessionLocal is None:
        raise Exception("Database engine is not configured.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Supabase Client Connection ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    print("WARNING: SUPABASE_URL or SUPABASE_KEY not found in environment variables.")
    supabase = None
