"""CommandVerb (spec §9.1.8). Mirror of content/command_verbs/*.md."""
from __future__ import annotations

import enum

from sqlalchemy import Enum, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from ..extensions import db
from ._mixins import UUIDPK


class CommandVerbTier(str, enum.Enum):
    recall = "recall"
    apply = "apply"
    analyse = "analyse"


class CommandVerb(UUIDPK, db.Model):
    __tablename__ = "command_verbs"

    verb: Mapped[str] = mapped_column(String(40), unique=True, nullable=False, index=True)
    tier: Mapped[CommandVerbTier] = mapped_column(
        Enum(CommandVerbTier, name="command_verb_tier"), nullable=False
    )
    definition: Mapped[str] = mapped_column(Text, nullable=False)
    expectations_by_ao: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    content_path: Mapped[str] = mapped_column(String(255), nullable=False)
