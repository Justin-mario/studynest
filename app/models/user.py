"""User — students and admins (spec §9.1.2)."""
from __future__ import annotations

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

import bcrypt
from flask_login import UserMixin
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db
from ._mixins import Timestamps, UUIDPK

if TYPE_CHECKING:
    from .cohort import Cohort


class Role(str, enum.Enum):
    student = "student"
    admin = "admin"


class User(UUIDPK, Timestamps, UserMixin, db.Model):
    __tablename__ = "users"

    handle: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    real_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role, name="user_role"), nullable=False, default=Role.student)
    cohort_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cohorts.id", ondelete="SET NULL"), nullable=True
    )
    must_change_password: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_signin_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    cohort: Mapped["Cohort | None"] = relationship(back_populates="users", foreign_keys=[cohort_id])

    def get_id(self) -> str:  # for Flask-Login
        return str(self.id)

    def set_password(self, plain: str) -> None:
        self.password_hash = bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, plain: str) -> bool:
        return bcrypt.checkpw(plain.encode("utf-8"), self.password_hash.encode("utf-8"))
