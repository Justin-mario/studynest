"""Authentication routes — sign in, sign out, change-password / handle.

Behaviour:
  * Sign-in is rate-limited to 5 attempts per minute per IP (FR-14).
  * On success, role drives the post-login redirect (FR-11):
      - admin    -> /admin/   (admin dashboard)
      - student  -> /dashboard/ (student dashboard)
  * If `must_change_password` is set, the user is redirected to
    /auth/change-password regardless of role (FR-12).
  * `?next=` is honoured but validated as an internal path only.
"""
from __future__ import annotations

from urllib.parse import urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select

from ..extensions import db, limiter
from ..models.user import Role, User

bp = Blueprint("auth", __name__, url_prefix="/auth")


def _is_safe_next(target: str | None) -> bool:
    """Only accept relative paths on this app — never external URLs."""
    if not target:
        return False
    parsed = urlparse(target)
    return parsed.scheme == "" and parsed.netloc == "" and target.startswith("/")


def _post_login_url(user: User) -> str:
    if user.must_change_password:
        return url_for("auth.change_password")
    if user.role == Role.admin:
        return url_for("admin.index")
    return url_for("dashboard.index")


@bp.route("/sign-in", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def sign_in():
    if current_user.is_authenticated:
        return redirect(_post_login_url(current_user))

    if request.method == "POST":
        handle = (request.form.get("handle") or "").strip()
        password = request.form.get("password") or ""

        user = db.session.execute(
            select(User).where(User.handle == handle)
        ).scalar_one_or_none()

        if user is None or not user.is_active or not user.check_password(password):
            flash("Wrong handle or password.", "error")
            return render_template("auth/sign_in.html"), 401

        login_user(user)

        # Honour ?next= if it's a safe internal path; otherwise role-based redirect.
        next_target = request.args.get("next") or request.form.get("next")
        if _is_safe_next(next_target):
            return redirect(next_target)
        return redirect(_post_login_url(user))

    return render_template("auth/sign_in.html")


@bp.route("/sign-out", methods=["POST"])
@login_required
def sign_out():
    logout_user()
    flash("Signed out.", "info")
    return redirect(url_for("public.landing"))


@bp.route("/change-password", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute", methods=["POST"])
def change_password():
    """Update handle, password, or both. Current password is always required.

    For an admin who wants to retire the seeded credentials this is the path:
    enter the current password, optionally change the handle, set a new
    password. Students arrive here on first sign-in via `must_change_password`.
    """
    if request.method == "POST":
        current_password = request.form.get("current_password") or ""
        new_password = request.form.get("new_password") or ""
        new_handle = (request.form.get("handle") or "").strip()

        if not current_user.check_password(current_password):
            flash("Current password is incorrect.", "error")
            return render_template("auth/change_password.html"), 401

        changes: list[str] = []

        # Optional handle change.
        if new_handle and new_handle != current_user.handle:
            taken = db.session.execute(
                select(User).where(User.handle == new_handle, User.id != current_user.id)
            ).scalar_one_or_none()
            if taken is not None:
                flash("That username is already in use.", "error")
                return render_template("auth/change_password.html"), 409
            current_user.handle = new_handle
            changes.append("username")

        # Optional password change.
        if new_password:
            if len(new_password) < 10:
                flash("New password must be at least 10 characters.", "error")
                return render_template("auth/change_password.html"), 400
            current_user.set_password(new_password)
            current_user.must_change_password = False
            changes.append("password")

        if not changes:
            # Forced change but the user submitted nothing changed.
            if current_user.must_change_password:
                flash("You must set a new password to continue.", "warning")
                return render_template("auth/change_password.html"), 400
            flash("Nothing to update.", "info")
            return render_template("auth/change_password.html")

        db.session.commit()
        flash("Updated " + " and ".join(changes) + ".", "success")
        return redirect(_post_login_url(current_user))

    return render_template("auth/change_password.html")
