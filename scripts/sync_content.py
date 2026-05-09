"""Manually sync content/ files into the DB.

Use after editing content outside of a running app, or once per deploy when
CONTENT_SYNC_ON_STARTUP is disabled in production.

    python scripts/sync_content.py
"""
from __future__ import annotations

from app import create_app
from app.services.content_loader import sync_all


def main() -> None:
    app = create_app()
    with app.app_context():
        sync_all()
        print("Content sync complete.")


if __name__ == "__main__":
    main()
