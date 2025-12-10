"""
# app/services/session_store.py
DEPRECATED: session store service disabled for now.


from typing import List, Optional
from uuid import uuid4
from datetime import datetime, timezone

from sqlalchemy import select, delete

from app.db.core import SessionLocal
from app.models.orm_models import SessionDB, MessageDB
from app.models.schemas import ChatMessage


def get_or_create_session(session_id: Optional[str]) -> str:
    """
    # Return an existing session_id if it exists, otherwise create a new session row.
    """
    db = SessionLocal()
    try:
        if session_id:
            existing = db.get(SessionDB, session_id)
            if existing:
                return session_id

        new_id = uuid4().hex
        new_session = SessionDB(id=new_id)
        db.add(new_session)
        db.commit()
        return new_id
    finally:
        db.close()


def get_history_for_session(session_id: str) -> List[ChatMessage]:
    """
    # Load the chat history for a given session_id from the database and
    # convert it into a list[ChatMessage] for your chat logic.
    """
    db = SessionLocal()
    try:
        stmt = (
            select(MessageDB)
            .where(MessageDB.session_id == session_id)
            .order_by(MessageDB.id.asc())
        )
        rows = db.execute(stmt).scalars().all()

        history: List[ChatMessage] = [
            ChatMessage(role=row.role, content=row.content)
            for row in rows
        ]
        return history
    finally:
        db.close()


def save_history_for_session(session_id: str, history: List[ChatMessage]) -> None:
    """
    # Persist the entire history for a session.

    # Easiest approach: wipe existing messages for this session and re-insert
    # from the in-memory history list.
    """
    db = SessionLocal()
    try:
        # Remove old messages for this session
        db.execute(
            delete(MessageDB).where(MessageDB.session_id == session_id)
        )

        # Insert the new history items
        now = datetime.now(timezone.utc)
        for msg in history:
            db.add(
                MessageDB(
                    session_id=session_id,
                    role=msg.role,
                    content=msg.content,
                    created_at=now,
                )
            )

        db.commit()
    finally:
        db.close()
"""