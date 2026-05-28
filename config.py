"""StudyNest configuration.

Environment-driven config. Read from .env in development; alwaysdata.com
sets env vars via the admin panel in production.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    # SQLite default keeps the file at project root so no `instance/` dir is
    # needed; gitignored by *.db. For Postgres, set DATABASE_URL in .env.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'studynest.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    SIGNIN_RATE_LIMIT = int(os.environ.get("SIGNIN_RATE_LIMIT", "5"))
    LLM_PER_USER_RATE_LIMIT = int(os.environ.get("LLM_PER_USER_RATE_LIMIT", "10"))

    LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "gemini")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

    CONTENT_DIR = BASE_DIR / "content"
    PROMPTS_DIR = BASE_DIR / "prompts"
    CONTENT_SYNC_ON_STARTUP = os.environ.get("CONTENT_SYNC_ON_STARTUP", "true").lower() == "true"

    # Initial admin account — seeded on first startup if no user with this handle
    # exists. After seeding, the admin can change handle and/or password via the
    # account page; these env vars are NOT consulted again.
    INITIAL_ADMIN_HANDLE = os.environ.get("INITIAL_ADMIN_HANDLE", "T-Level Tutor")
    INITIAL_ADMIN_PASSWORD = os.environ.get("INITIAL_ADMIN_PASSWORD", "Best!Tutor@2026")

    # In dev, create missing tables on startup. Production should rely on
    # Alembic migrations and set this to false.
    AUTO_CREATE_TABLES = os.environ.get("AUTO_CREATE_TABLES", "true").lower() == "true"


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # http in dev


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False
    CONTENT_SYNC_ON_STARTUP = False


class ProductionConfig(Config):
    DEBUG = False


def get_config() -> type[Config]:
    env = os.environ.get("FLASK_ENV", "development").lower()
    return {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }.get(env, DevelopmentConfig)
