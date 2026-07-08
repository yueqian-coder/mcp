import pytest
from pydantic import ValidationError

from researchgraphos.config import LLMSettings
from researchgraphos.core import (
    DEFAULT_PROJECT_QUESTION,
    build_default_state,
    build_deterministic_report,
    normalize_project_state,
    report_to_context_markdown,
    run_research_state_agent,
    state_signature,
)


def test_build_default_state_applies_source_status_overrides():
    state = build_default_state({"repo_lightrag": "reproduced"})

    repo = next(source for source in state["sources"] if source.id == "repo_lightrag")
    report = build_deterministic_report(state)

    assert repo.status == "reproduced"
    assert all(rec.target != "HKUDS/LightRAG" for rec in report.recommendations)


def test_report_to_context_markdown_exports_agent_readable_context():
    report = build_deterministic_report()

    markdown = report_to_context_markdown(report)

    assert "# Failure-aware GraphRAG Router" in markdown
    assert "## Missing Methods / Evidence" in markdown
    assert "## Recommended Next Steps" in markdown
    assert "EA-GraphRAG" in markdown


def test_run_research_state_agent_returns_fallback_result_when_api_is_unconfigured():
    state = build_default_state()
    settings = LLMSettings(
        provider="openai_compatible",
        base_url="",
        api_key="",
        model="",
    )

    result = run_research_state_agent(
        question=DEFAULT_PROJECT_QUESTION,
        state=state,
        settings=settings,
    )

    assert result.used_fallback
    assert "incomplete" in result.fallback_reason.lower()
    assert result.report.short_answer == build_deterministic_report(state).short_answer


def test_state_signature_changes_when_model_changes():
    state = build_default_state()
    first_settings = LLMSettings(
        provider="openai_compatible",
        base_url="https://example.test/v1",
        api_key="key",
        model="model-a",
    )
    second_settings = first_settings.__class__(
        provider=first_settings.provider,
        base_url=first_settings.base_url,
        api_key=first_settings.api_key,
        model="model-b",
    )

    first = state_signature(state, DEFAULT_PROJECT_QUESTION, settings=first_settings)
    second = state_signature(state, DEFAULT_PROJECT_QUESTION, settings=second_settings)

    assert first != second


def test_state_signature_does_not_include_api_endpoint_or_key():
    state = build_default_state()
    settings = LLMSettings(
        provider="openai_compatible",
        base_url="https://private-provider.example/v1",
        api_key="secret-key",
        model="model-a",
    )

    signature = repr(state_signature(state, DEFAULT_PROJECT_QUESTION, settings=settings))

    assert "private-provider" not in signature
    assert "secret-key" not in signature


def test_normalize_project_state_accepts_json_style_payload():
    state = normalize_project_state(
        {
            "project": {
                "id": "proj_custom",
                "name": "Custom Project",
                "goal": "Test JSON-style state.",
                "keywords": ["GraphRAG"],
            },
            "sources": [
                {
                    "id": "paper_custom",
                    "title": "Custom Paper",
                    "kind": "paper",
                    "status": "read",
                    "citation": "Custom citation",
                }
            ],
        }
    )

    assert state["project"].id == "proj_custom"
    assert state["sources"][0].id == "paper_custom"


def test_build_deterministic_report_rejects_invalid_empty_state():
    with pytest.raises(ValidationError):
        build_deterministic_report({})


class LeakyProvider:
    def complete_json(self, messages):
        raise RuntimeError("failed against https://private-provider.example/v1 with secret-key")


def test_run_research_state_agent_returns_public_fallback_reason():
    state = build_default_state()
    settings = LLMSettings(
        provider="openai_compatible",
        base_url="https://private-provider.example/v1",
        api_key="secret-key",
        model="model-a",
    )

    result = run_research_state_agent(
        question=DEFAULT_PROJECT_QUESTION,
        state=state,
        settings=settings,
        provider=LeakyProvider(),
    )

    assert result.used_fallback
    assert result.fallback_reason == "API agent failed"
    assert "private-provider" not in result.fallback_reason
    assert "secret-key" not in result.fallback_reason
