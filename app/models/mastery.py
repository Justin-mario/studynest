"""Mastery (spec §9.1.13). Per-user, per-topic OR per-command-verb mastery estimate.

Exclusivity invariant: exactly one of topic_id / command_verb_id is non-null.
Enforced via DB CHECK constraint and at write-time in the scoring service.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..extensions import db
from ._mixins import UUIDPK


class Mastery(UUIDPK, db.Model):
    __tablename__ = "mastery"
    __table_args__ = (
        CheckConstraint(
            "(topic_id IS NOT NULL)::int + (command_verb_id IS NOT NULL)::int = 1",
            name="mastery_exactly_one_target",
        ),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    topic_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), nullable=True
    )
    command_verb_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("command_verbs.id", ondelete="CASCADE"), nullable=True
    )
    score: Mapped[float] = mapped_column(Numeric(5, 4), nullable=False, default=0)
    attempts_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_practised_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_review_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
