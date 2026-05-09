"""Sync file-based content (Markdown topics, YAML quizzes, command-verb guides,
misconceptions, specification) into Postgres mirror tables.

Source-of-truth lives on disk under content/ and prompts/. Mirror tables exist
so that questions/topics can be foreign-keyed from per-user data (attempts,
mastery, sessions, transcripts).

Sync runs on app startup when CONTENT_SYNC_ON_STARTUP is true. In production,
prefer running `python scripts/sync_content.py` once per deploy and turning
the startup hook off.
"""
from __future__ import annotations

import logging
from pathlib import Path

from flask import current_app

log = logging.getLogger(__name__)


def sync_all() -> None:
    """Run every sub-syncer in dependency order."""
    content_dir: Path = current_app.config["CONTENT_DIR"]
    if not content_dir.exists():
        log.warning("Content dir %s does not exist; skipping sync.", content_dir)
        return

    sync_specification(content_dir / "specification.yaml")
    sync_command_verbs(content_dir / "command_verbs")
    sync_topics(content_dir / "topics")
    sync_questions(content_dir / "quizzes")
    sync_misconceptions(content_dir / "misconceptions.yaml")


def sync_specification(path: Path) -> None:
    """Load specification, performance_outcomes, assessment_objectives from YAML."""
    # TODO: parse YAML, upsert into specifications/performance_outcomes/assessment_objectives.


def sync_command_verbs(dir_path: Path) -> None:
    """Load one command-verb Markdown file per verb (with YAML frontmatter)."""
    # TODO: walk dir, parse frontmatter via python-frontmatter, upsert CommandVerb.


def sync_topics(dir_path: Path) -> None:
    """Load topic Markdown files under content/topics/{paper}/{slug}.md."""
    # TODO: walk dir, parse frontmatter, upsert Topic + TopicPOLink rows.


def sync_questions(dir_path: Path) -> None:
    """Load YAML quiz files under content/quizzes/{paper}/{slug}-quiz.yaml."""
    # TODO: walk dir, validate against schema, upsert Question rows.


def sync_misconceptions(path: Path) -> None:
    """Load misconceptions library from a single YAML file."""
    # TODO: parse YAML, upsert Misconception rows keyed by external_id.
