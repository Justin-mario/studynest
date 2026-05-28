"""Session (spec §9.1.11). A user's interaction with one of the learning surfaces."""
from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..extensions import db
from ._mixins import UUIDPK


class SessionType(str, enum.Enum):
    topic_quiz = "topic_quiz"
    mixed_quiz = "mixed_quiz"
    past_question_practice = "past_question_practice"
    spaced_repetition = "spaced_repetition"
    explainit = "explainit"
    command_verbs_diagnostic = "command_verbs_diagnostic"
    command_verbs_practice = "command_verbs_practice"


class Session(UUIDPK, db.Model):
    __tablename__ = "sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    type: Mapped[SessionType] = mapped_column(Enum(SessionType, name="session_type"), nullable=False)
    context_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(), nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    summary: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
