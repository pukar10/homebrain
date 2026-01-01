"""
app/db/core.py
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from backend.app.settings import get_settings

settings = get_settings()

class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass

SQLengine = create_engine(
    settings.database_url,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(
    bind=SQLengine, 
    autoflush=False, 
    autocommit=False,
)
