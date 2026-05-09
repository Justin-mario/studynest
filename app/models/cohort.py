"""Cohort — a group of students taught together (spec §9.1.1)."""
from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db
from ._mixins import Timestamps, UUIDPK

if TYPE_CHECKING:
    from .user import User


class Cohort(UUIDPK, Timestamps, db.Model):
    __tablename__ = "cohorts"

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    academic_year: Mapped[str] = mapped_column(String(16), nullable=False)
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    users: Mapped[list["User"]] = relationship(back_populates="cohort", foreign_keys="User.cohort_id")
