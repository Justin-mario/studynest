"""Core Paper module — Core 1 and Core 2 topic browsing, content, and quizzes."""
from __future__ import annotations

from flask import Blueprint, abort, render_template
from flask_login import login_required

bp = Blueprint("core_paper", __name__, url_prefix="/core-paper")


@bp.route("/")
@login_required
def index():
    return render_template("core_paper/index.html")


@bp.route("/<int:paper>/")
@login_required
def paper(paper: int):
    if paper not in (1, 2):
        abort(404)
    return render_template("core_paper/paper.html", paper=paper)


@bp.route("/<int:paper>/<slug>/")
@login_required
def topic(paper: int, slug: str):
    # TODO FR-30: topic page with overview, spec mapping, content, quiz, extended-response.
    return render_template("core_paper/topic.html", paper=paper, slug=slug)


@bp.route("/<int:paper>/<slug>/quiz", methods=["GET", "POST"])
@login_required
def quiz(paper: int, slug: str):
    # TODO FR-31..FR-37: mixed-format quiz, persisted attempts, mastery update.
    return render_template("core_paper/quiz.html", paper=paper, slug=slug)
