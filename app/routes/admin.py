"""Admin Dashboard — cohort analytics, student management, system settings.

All routes require role='admin'. A `before_request` guard rejects students.
See spec §6.8 (FR-80..FR-94) and §12.2.
"""
from __future__ import annotations

from flask import Blueprint, abort, render_template
from flask_login import current_user, login_required

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.before_request
@login_required
def require_admin():
    if not current_user.is_authenticated or current_user.role != "admin":
        abort(403)


@bp.route("/")
def index():
    # TODO FR-80: at-a-glance stats and links.
    return render_template("admin/dashboard.html")


@bp.route("/cohorts/")
def cohorts():
    return render_template("admin/cohorts.html")


@bp.route("/students/")
def students():
    # TODO FR-81/FR-86/FR-90/FR-91.
    return render_template("admin/students.html")


@bp.route("/students/new", methods=["GET", "POST"])
def student_new():
    # TODO FR-83.
    return render_template("admin/student_new.html")


@bp.route("/students/import", methods=["GET", "POST"])
def student_import():
    # TODO FR-84: CSV bulk import.
    return render_template("admin/student_import.html")


@bp.route("/students/<student_id>")
def student_detail(student_id: str):
    # TODO FR-86.
    return render_template("admin/student_detail.html", student_id=student_id)


@bp.route("/analytics/")
def analytics():
    # TODO FR-85/FR-92.
    return render_template("admin/analytics.html")


@bp.route("/settings/")
def settings():
    return render_template("admin/settings.html")
