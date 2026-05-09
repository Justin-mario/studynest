"""Scoring and mastery updates.

Pure functions where possible; DB writes wrapped in `update_mastery_from_attempt`.
FR-100: mastery updates automatically from attempt results.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass


@dataclass
class GradedAttempt:
    score: float  # normalised 0..1
    max_score: int
    feedback: dict


def grade_multiple_choice(*, correct_index: int, chosen_index: int) -> GradedAttempt:
    """FR-32: deterministic, instant feedback for MCQs."""
    correct = chosen_index == correct_index
    return GradedAttempt(
        score=1.0 if correct else 0.0,
        max_score=1,
        feedback={"correct": correct},
    )


def update_mastery_from_attempt(
    *, user_id: uuid.UUID, topic_id: uuid.UUID | None, command_verb_id: uuid.UUID | None,
    score: float,
) -> None:
    """FR-100/FR-101: blend the new attempt into the user's mastery for the target,
    recompute next_review_at via spaced_repetition.next_review."""
    # TODO: load Mastery row (or create), apply EMA-style update, set last_practised_at,
    # call spaced_repetition.next_review() to set next_review_at.
    raise NotImplementedError
