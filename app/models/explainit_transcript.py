"""ExplainIT transcript (spec §9.1.14). Full conversation + misconception state at session end."""
from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..extensions import db
from ._mixins import UUIDPK


class ExplainItEndReason(str, enum.Enum):
    completed = "completed"
    student_ended = "student_ended"
    turn_limit = "turn_limit"


class ExplainItTranscript(UUIDPK, db.Model):
    __tablename__ = "explainit_transcripts"

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    misconceptions_planned: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    misconceptions_resolved: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    transcript: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    end_reason: Mapped[ExplainItEndReason] = mapped_column(
        Enum(ExplainItEndReason, name="explainit_end_reason"), nullable=False
    )
    student_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
