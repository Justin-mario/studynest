"""ExplainIT state machine.

Per spec §11.2: persona consistency and misconception tracking are NOT delegated
to the LLM. The state machine here owns:
  - which misconceptions were planned for this session (drawn from the topic's
    curated misconception library)
  - which misconceptions are still unresolved
  - turn count and end-condition checks (FR-55: completed / student_ended / turn_limit)

Each turn:
  1. caller passes student_message + current state into `take_turn`
  2. engine consults `llm_client.explainit_turn` for the AI's reply
  3. engine inspects the student's message + AI reply, marks misconceptions
     as resolved if the student's explanation addresses them
  4. engine returns updated state + AI reply for rendering
"""
from __future__ import annotations

import enum
import uuid
from dataclasses import dataclass, field
from typing import Iterable


class TurnOutcome(str, enum.Enum):
    continue_session = "continue"
    completed = "completed"
    student_ended = "student_ended"
    turn_limit = "turn_limit"


@dataclass
class ExplainItState:
    topic_id: uuid.UUID
    persona: str = "Sam"
    turn_count: int = 0
    max_turns: int = 20
    misconceptions_planned: list[str] = field(default_factory=list)
    misconceptions_resolved: list[str] = field(default_factory=list)
    transcript: list[dict] = field(default_factory=list)


def initialise_session(
    *, topic_id: uuid.UUID, planned_misconceptions: Iterable[str], max_turns: int = 20
) -> ExplainItState:
    """Create an ExplainItState for a fresh session."""
    return ExplainItState(
        topic_id=topic_id,
        misconceptions_planned=list(planned_misconceptions),
        max_turns=max_turns,
    )


def take_turn(state: ExplainItState, student_message: str) -> tuple[ExplainItState, str, TurnOutcome]:
    """Advance one turn. Returns the new state, the AI's reply, and the outcome."""
    # TODO: call llm_client.explainit_turn, append to transcript, run misconception
    # resolution check, increment turn count, evaluate end conditions.
    raise NotImplementedError


def evaluate_end_conditions(state: ExplainItState, student_ended: bool = False) -> TurnOutcome:
    if student_ended:
        return TurnOutcome.student_ended
    if state.turn_count >= state.max_turns:
        return TurnOutcome.turn_limit
    if set(state.misconceptions_resolved) >= set(state.misconceptions_planned):
        return TurnOutcome.completed
    return TurnOutcome.continue_session
