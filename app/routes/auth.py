"""Authentication routes: sign in, sign out, forced password change."""
from __future__ import annotations

from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, logout_user

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    # TODO FR-10/FR-11/FR-14: rate-limited sign-in, role-based redirect.
    return render_template("auth/sign_in.html")


@bp.route("/sign-out", methods=["POST"])
@login_required
def sign_out():
    logout_user()
    return redirect(url_for("public.landing"))


@bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    # TODO FR-12: forced first-sign-in password change.
    return render_template("auth/change_password.html")
