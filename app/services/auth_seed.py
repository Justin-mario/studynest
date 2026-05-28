"""Idempotent first-run seeding for the initial admin account.

Runs in the application factory after extensions are initialised. If no user
with INITIAL_ADMIN_HANDLE exists, one is created with INITIAL_ADMIN_PASSWORD.
If an admin already exists with that handle, this is a no-op — we never reset
a real admin's password from env config.

The seeded admin starts with ``must_change_password = False`` so the static
credentials from the spec work immediately; the admin can change handle and
password later via ``/auth/change-password``.
"""
from __future__ import annotations

import logging

from flask import current_app
from sqlalchemy import select

from ..extensions import db
from ..models.user import Role, User

log = logging.getLogger(__name__)


def ensure_tables() -> None:
    """Create any missing tables in dev. Prefer Alembic migrations in production."""
    if current_app.config.get("AUTO_CREATE_TABLES"):
        # Importing the models package registers every model on the Base metadata.
        from .. import models  # noqa: F401

        db.create_all()


def ensure_admin_account() -> None:
    """Seed the initial admin account if it doesn't already exist."""
    handle = current_app.config["INITIAL_ADMIN_HANDLE"]
    password = current_app.config["INITIAL_ADMIN_PASSWORD"]

    existing = db.session.execute(
        select(User).where(User.handle == handle)
    ).scalar_one_or_none()
    if existing is not None:
        # Don't reset the admin's password from env — they may have changed it.
        return

    admin = User(
        handle=handle,
        role=Role.admin,
        must_change_password=False,
        is_active=True,
    )
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    log.info("Seeded initial admin account with handle %r", handle)
