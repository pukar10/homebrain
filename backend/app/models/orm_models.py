from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, ForeignKey, BigInteger

from app.db.core import Base


# Redo table to be keyed by thread_id for stats.
# Deprecated at the moment; using LangGraph's checkpointer instead.
class SessionDB(Base):
    """
    Represents a chat session in the database.

    One SessionDB -> many MessageDB rows.
    """

    __tablename__ = "sessions"

    # Columns
    id: Mapped[str] = mapped_column(String, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # SessionDB model has a one-to-many relationship with MessageDB
    messages: Mapped[list["MessageDB"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )


# Deprecated at the moment; using LangGraph's checkpointer instead.
class MessageDB(Base):
    
    __tablename__ = "messages"

    # Columns
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(
        String, ForeignKey("sessions.id", ondelete="CASCADE"), index=True
    )
    role: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Every MessageDB belongs to one SessionDB
    session: Mapped[SessionDB] = relationship(back_populates="messages")
