import json
from typing import Protocol

from pydantic import ValidationError

from researchgraphos.models import ResearchStateReport
from researchgraphos.report import build_research_state_report


class JSONProvider(Protocol):
    def complete_json(self, messages: list[dict[str, str]]) -> dict:
        """Return JSON-compatible data from a chat completion."""


class ResearchStateAgent:
    def __init__(self, provider: JSONProvider | None = None):
        self.provider = provider

    def answer(self, question: str, state: dict) -> ResearchStateReport:
        fallback = build_research_state_report(state)
        if self.provider is None:
            return fallback

        messages = self._build_messages(question=question, state=state)
        try:
            payload = self.provider.complete_json(messages)
            return ResearchStateReport.model_validate(payload)
        except (RuntimeError, ValidationError, ValueError, TypeError):
            return fallback

    def _build_messages(self, question: str, state: dict) -> list[dict[str, str]]:
        project = state["project"].model_dump()
        sources = [source.model_dump() for source in state["sources"]]
        user_payload = {
            "question": question,
            "project": project,
            "sources": sources,
        }

        return [
            {
                "role": "system",
                "content": (
                    "You are the Research State Agent inside ResearchGraphOS. "
                    "Return only JSON that matches the ResearchStateReport schema. "
                    "Explain covered methods by source, missing methods/evidence, novelty overlap, "
                    "status questions, recommendations, and evidence paths. "
                    "Do not overclaim novelty; use novelty risk instead."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(user_payload, ensure_ascii=False),
            },
        ]
