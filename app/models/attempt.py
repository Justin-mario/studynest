"""Attempt (spec §9.1.12). One row per question response."""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..extensions import db
from ._mixins import UUIDPK


class Attempt(UUIDPK, db.Model):
    __tablename__ = "attempts"

    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    response_text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    response_voice_used: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    score: Mapped[float] = mapped_column(Numeric(5, 4), nullable=False, default=0)
    max_score: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    feedback: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    llm_provider: Mapped[str | None] = mapped_column(String(40), nullable=True)
    llm_tokens_used: Mapped[int | None] = mapped_column(Integer, nullable=True)
    attempted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
