"""Student Dashboard — personalised home for authenticated students."""
from __future__ import annotations

from flask import Blueprint, render_template
from flask_login import current_user, login_required

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.route("/")
@login_required
def index():
    # TODO FR-20..FR-26: greeting, recommended next session, mastery overview,
    # weak spots, recent activity, soft consistency indicator.
    return render_template("student/dashboard.html", user=current_user)
