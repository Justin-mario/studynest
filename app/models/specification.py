"""Specification, PerformanceOutcome, AssessmentObjective (spec §9.1.3-9.1.5).

Mirror of `content/specification.yaml`. Synced into DB on startup so other
tables can foreign-key to performance outcomes and AOs.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..extensions import db
from ._mixins import UUIDPK


class Specification(UUIDPK, db.Model):
    __tablename__ = "specifications"

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    loaded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class PerformanceOutcome(UUIDPK, db.Model):
    __tablename__ = "performance_outcomes"

    specification_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("specifications.id", ondelete="CASCADE"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class AssessmentObjective(UUIDPK, db.Model):
    __tablename__ = "assessment_objectives"

    code: Mapped[str] = mapped_column(String(8), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
