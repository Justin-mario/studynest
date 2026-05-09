"""Revision section — mixed quizzes, past-question practice, spaced-repetition queue."""
from __future__ import annotations

from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint("revision", __name__, url_prefix="/revision")


@bp.route("/")
@login_required
def index():
    return render_template("revision/index.html")


@bp.route("/mixed-quizzes")
@login_required
def mixed_quizzes():
    # TODO FR-71: mastery-weighted question selection across topics.
    return render_template("revision/mixed_quizzes.html")


@bp.route("/past-question-practice")
@login_required
def past_question_practice():
    # TODO FR-72/FR-74: extended-response practice with voice input.
    return render_template("revision/past_question_practice.html")


@bp.route("/spaced-repetition")
@login_required
def spaced_repetition():
    # TODO FR-73 / FR-101: surface items prioritised by next_review_at.
    return render_template("revision/spaced_repetition.html")
