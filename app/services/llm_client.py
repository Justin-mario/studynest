"""LLM client with provider abstraction.

NFR-19 + spec §11.1: provider switch by configuration only. To add or change
providers, implement the Provider protocol and register it in `get_provider`.

Public API:
    grade_short_answer(prompt, model_answer, response, rubric) -> dict
    feedback_extended_response(prompt, response, command_verb, aos) -> dict
    explainit_turn(state, student_message) -> dict

Each public function loads its system prompt from prompts/, calls the configured
provider, and returns a structured result. FR-102 requires server-side only;
FR-103 requires per-user rate limits applied by the caller.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from flask import current_app

log = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    text: str
    provider: str
    model: str
    tokens_used: int | None = None
    latency_ms: int | None = None
    request_id: str | None = None


class Provider(Protocol):
    name: str
    model: str

    def complete(self, system: str, user: str, **kwargs: Any) -> LLMResponse: ...


class GeminiProvider:
    name = "gemini"

    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def complete(self, system: str, user: str, **kwargs: Any) -> LLMResponse:
        # TODO: implement with google-genai SDK; log provider/model/tokens/latency/request_id.
        raise NotImplementedError


class GroqProvider:
    name = "groq"

    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def complete(self, system: str, user: str, **kwargs: Any) -> LLMResponse:
        # TODO: implement with groq SDK.
        raise NotImplementedError


def get_provider() -> Provider:
    cfg = current_app.config
    name = cfg["LLM_PROVIDER"].lower()
    if name == "gemini":
        return GeminiProvider(cfg["GEMINI_API_KEY"], cfg["GEMINI_MODEL"])
    if name == "groq":
        return GroqProvider(cfg["GROQ_API_KEY"], cfg["GROQ_MODEL"])
    raise ValueError(f"Unknown LLM_PROVIDER: {name!r}")


def _load_prompt(name: str) -> str:
    path: Path = current_app.config["PROMPTS_DIR"] / name
    return path.read_text(encoding="utf-8")


# ---------- Public, feature-level API ----------


def grade_short_answer(
    *, prompt: str, model_answer: str, response: str, rubric: dict
) -> dict:
    """FR-33: rubric-graded short-answer scoring.

    Returns: {"score": float in [0,1], "feedback": str, "criteria": [...], "provider": str}
    """
    # TODO: build user message from inputs, call get_provider().complete(...)
    # parse structured JSON output, log call.
    raise NotImplementedError


def feedback_extended_response(
    *, prompt: str, response: str, command_verb: str, aos: list[str]
) -> dict:
    """FR-34/FR-47: command-verb-aware extended-response feedback.

    Returns: {"verb": str, "aos_hit": [...], "points": [...], "suggestions": [...], "provider": str}
    """
    raise NotImplementedError


def explainit_turn(*, state: dict, student_message: str) -> dict:
    """FR-52..FR-55: one ExplainIT turn.

    `state` carries persona id, planned/resolved misconception ids, turn count,
    transcript so far. The state machine lives in explainit_engine; this function
    only turns state + message into one model call.

    Returns: {"reply": str, "intent": "ask_followup" | "accept_resolution" | "end_session", "provider": str}
    """
    raise NotImplementedError
