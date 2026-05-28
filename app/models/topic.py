"""Topic and TopicPOLink (spec §9.1.6, §9.1.7).

Mirror of Markdown files under content/topics/. Synced on startup.
"""
from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..extensions import db
from ._mixins import UUIDPK


class Topic(UUIDPK, db.Model):
    __tablename__ = "topics"

    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    core_paper: Mapped[int] = mapped_column(Integer, nullable=False)
    topic_number: Mapped[int] = mapped_column(Integer, nullable=False)
    estimated_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=20)
    overview: Mapped[str] = mapped_column(Text, nullable=False, default="")
    explainit_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    content_path: Mapped[str] = mapped_column(String(255), nullable=False)
    last_updated: Mapped[date | None] = mapped_column(Date, nullable=True)
    synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class TopicPOLink(db.Model):
    __tablename__ = "topic_po_links"

    topic_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True
    )
    performance_outcome_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(),
        ForeignKey("performance_outcomes.id", ondelete="CASCADE"),
        primary_key=True,
    )
