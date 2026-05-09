"""Tests for the spaced-repetition scheduler."""
from __future__ import annotations

from datetime import datetime, timezone

from app.services.spaced_repetition import next_review


def test_low_score_schedules_soon():
    now = datetime(2026, 5, 1, tzinfo=timezone.utc)
    result = next_review(current_score=0.2, attempts_count=0, now=now)
    delta = result - now
    assert 0 < delta.total_seconds() <= 24 * 3600 + 1


def test_high_score_schedules_far_out():
    now = datetime(2026, 5, 1, tzinfo=timezone.utc)
    result = next_review(current_score=0.95, attempts_count=0, now=now)
    delta = result - now
    assert delta.days >= 14


def test_more_attempts_extends_interval():
    now = datetime(2026, 5, 1, tzinfo=timezone.utc)
    a = next_review(current_score=0.7, attempts_count=0, now=now)
    b = next_review(current_score=0.7, attempts_count=5, now=now)
    assert b > a
