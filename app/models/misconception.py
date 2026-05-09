"""Misconception (spec §9.1.10). Mirror of content/misconceptions.yaml. Used by ExplainIT."""
from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..extensions import db
from ._mixins import UUIDPK


class Misconception(UUIDPK, db.Model):
    __tablename__ = "misconceptions"

    external_id: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    typical_response_pattern: Mapped[str] = mapped_column(Text, nullable=False)
    probing_questions: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    correct_understanding: Mapped[str] = mapped_column(Text, nullable=False)
