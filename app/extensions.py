"""Flask extension singletons.

Defined here so any module can import them without going through the app factory.
"""
from __future__ import annotations

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Single declarative base shared by every model."""


db = SQLAlchemy(model_class=Base)
csrf = CSRFProtect()
login_manager = LoginManager()

# In-memory storage is fine for single-process dev; explicitly set so
# Flask-Limiter doesn't warn at startup. For production at scale, swap
# to Redis (set storage_uri to e.g. "redis://localhost:6379").
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
    storage_uri="memory://",
)
