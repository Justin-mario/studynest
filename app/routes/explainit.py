"""ExplainIT — teach-the-AI feature.

The student selects a topic and engages a confused AI character ('Sam') in a
probing conversation. The AI holds curated misconceptions and pursues
follow-up questions until the student demonstrates understanding.

State of the conversation (which misconceptions remain unresolved) is tracked
in the explainit_engine service, not relied upon from the LLM. See spec §6.6 / §11.2.
"""
from __future__ import annotations

from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint("explainit", __name__, url_prefix="/explainit")


@bp.route("/")
@login_required
def index():
    # TODO FR-50/FR-51: list topics with explainit_enabled=true.
    return render_template("explainit/index.html")


@bp.route("/session/<topic_slug>", methods=["GET"])
@login_required
def session_view(topic_slug: str):
    # TODO FR-52..FR-60: live session view; HTMX-driven turn updates.
    return render_template("explainit/session.html", topic_slug=topic_slug)


@bp.route("/session/<topic_slug>/turn", methods=["POST"])
@login_required
def session_turn(topic_slug: str):
    # TODO FR-54: pursue follow-ups; advance misconception state.
    return render_template("explainit/_turn.html", topic_slug=topic_slug)


@bp.route("/transcripts/")
@login_required
def transcripts():
    # TODO FR-58: review past ExplainIT transcripts.
    return render_template("explainit/transcripts.html")
