"""Exam Technique → Command Verbs.

Top-level section. First feature: Command Verbs (diagnostic, guides, practice, quick reference).
Future siblings (time management, structuring extended responses, reading the question,
self-marking) are out of scope for the first release — see spec §6.5.
"""
from __future__ import annotations

from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint("exam_technique", __name__, url_prefix="/exam-technique")


@bp.route("/")
@login_required
def index():
    return render_template("exam_technique/index.html")


@bp.route("/command-verbs/")
@login_required
def command_verbs_index():
    # TODO FR-41: links to Diagnostic, Guide, Practice, Quick Reference.
    return render_template("exam_technique/command_verbs/index.html")


@bp.route("/command-verbs/diagnostic", methods=["GET", "POST"])
@login_required
def diagnostic():
    # TODO FR-42..FR-44: 10-12 prompts, repeatable, per-verb strength report.
    return render_template("exam_technique/command_verbs/diagnostic.html")


@bp.route("/command-verbs/guide/<verb>")
@login_required
def verb_guide(verb: str):
    # TODO FR-45: definition, AO expectations, worked example, common mistakes, mini-exercise.
    return render_template("exam_technique/command_verbs/guide.html", verb=verb)


@bp.route("/command-verbs/practice", methods=["GET", "POST"])
@login_required
def practice():
    # TODO FR-46/FR-47: text/voice input; verb- and AO-aware feedback.
    return render_template("exam_technique/command_verbs/practice.html")


@bp.route("/command-verbs/quick-reference")
@login_required
def quick_reference():
    # TODO FR-48: single-page card of all verbs.
    return render_template("exam_technique/command_verbs/quick_reference.html")
