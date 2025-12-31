"""
app/db/core.py
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import get_settings

settings = get_settings()

class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass

engine = create_engine(
    settings.database_url,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine, 
    autoflush=False, 
    autocommit=False,
)
