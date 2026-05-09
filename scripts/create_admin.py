"""Create the first admin account.

    python scripts/create_admin.py <handle> <password>

Idempotent: re-running with the same handle resets the password.
"""
from __future__ import annotations

import sys

from app import create_app
from app.extensions import db
from app.models.user import Role, User


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: create_admin.py <handle> <password>", file=sys.stderr)
        return 2

    handle, password = argv[1], argv[2]
    app = create_app()
    with app.app_context():
        user = db.session.query(User).filter_by(handle=handle).one_or_none()
        if user is None:
            user = User(handle=handle, role=Role.admin)
            db.session.add(user)
        user.role = Role.admin
        user.must_change_password = False
        user.is_active = True
        user.set_password(password)
        db.session.commit()
        print(f"Admin {handle!r} ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
