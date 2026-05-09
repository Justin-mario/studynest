"""Spaced-repetition scheduling.

A simple SM-2-derived schedule is enough for v1. FR-73/FR-101: next_review_at
combines previous score and time-since-last-review. Algorithm choice is
deliberately swappable behind `next_review`.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone


def next_review(*, current_score: float, attempts_count: int, now: datetime | None = None) -> datetime:
    """Return when this item should next surface.

    score in [0,1]; higher score => longer interval. Intervals roughly:
      <0.4 -> 1 day, <0.6 -> 3 days, <0.8 -> 7 days, else -> 14 days,
    multiplied by a small factor that grows with attempts_count.
    """
    now = now or datetime.now(timezone.utc)
    if current_score < 0.4:
        days = 1
    elif current_score < 0.6:
        days = 3
    elif current_score < 0.8:
        days = 7
    else:
        days = 14
    factor = 1 + min(attempts_count, 6) * 0.15
    return now + timedelta(days=days * factor)
