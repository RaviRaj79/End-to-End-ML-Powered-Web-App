import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import DeclarativeBase, sessionmaker

def default_database_url() -> str:
    """Store local data outside the project directory, which may be read-only."""
    data_root = Path(os.getenv("LOCALAPPDATA", Path.home())) / "TalentMatchAI"
    data_root.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{(data_root / 'talentmatch.db').as_posix()}"


DATABASE_URL = os.getenv("DATABASE_URL") or default_database_url()
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
# The in-memory mode is intentionally supported for fast, isolated tests.
engine_options = {"connect_args": connect_args}
if DATABASE_URL == "sqlite://":
    engine_options["poolclass"] = StaticPool
engine = create_engine(DATABASE_URL, **engine_options)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
