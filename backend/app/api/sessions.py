"""
app/api/sessions.py
DEPRECATED: session endpoints disabled for now.

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.db.core import SessionLocal
from app.models.orm_models import SessionDB, MessageDB
from app.models.schemas import SessionSummary, SessionDetail, ChatMessage

router = APIRouter(prefix="/api", tags=["sessions"])


@router.get("/sessions", response_model=list[SessionSummary])
def list_sessions():
    db = SessionLocal()
    try:
        rows = db.execute(select(SessionDB).order_by(SessionDB.created_at.desc())).scalars().all()
        return [
            SessionSummary(
                id=s.id,
                created_at=s.created_at,
            )
            for s in rows
        ]
    finally:
        db.close()


@router.get("/sessions/{session_id}", response_model=SessionDetail)
def get_session(session_id: str) -> SessionDetail:
    
    db = SessionLocal()

    try:
        session = db.get(SessionDB, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        stmt = (
            select(MessageDB)
            .where(MessageDB.session_id == session_id)
            .order_by(MessageDB.id.asc())
        )
        rows = db.execute(stmt).scalars().all()

        messages = [
            ChatMessage(role=m.role, content=m.content) 
            for m in rows
        ]

        return SessionDetail(
            id=session.id,
            created_at=session.created_at,
            messages=messages,
        )
    finally:
        db.close()
"""