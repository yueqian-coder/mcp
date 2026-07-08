import json

import pytest
from pydantic import ValidationError

from researchgraphos.core import build_default_state
from researchgraphos.mcp_bridge import (
    get_context_markdown,
    get_gap_report_payload,
    get_projects_payload,
)


def test_get_projects_payload_returns_json_serializable_projects():
    payload = get_projects_payload()

    json.dumps(payload)
    assert payload[0]["id"] == "proj_graphrag_router"
    assert payload[0]["name"] == "Failure-aware GraphRAG Router"


def test_get_gap_report_payload_returns_read_only_report_data():
    payload = get_gap_report_payload()

    json.dumps(payload)
    assert payload["project"]["id"] == "proj_graphrag_router"
    assert payload["gaps"]
    assert payload["recommendations"]


def test_get_context_markdown_returns_agent_context():
    markdown = get_context_markdown()

    assert markdown.startswith("# Failure-aware GraphRAG Router")
    assert "## Recommended Next Steps" in markdown


def test_bridge_rejects_invalid_empty_state_instead_of_using_demo():
    with pytest.raises(ValidationError):
        get_projects_payload({})


def test_project_payload_mutation_does_not_modify_source_state():
    state = build_default_state()

    payload = get_projects_payload(state)
    payload[0]["keywords"].append("mutated")

    assert "mutated" not in state["project"].keywords


def test_gap_report_payload_respects_custom_source_statuses():
    state = build_default_state({"repo_lightrag": "reproduced"})

    payload = get_gap_report_payload(state)

    assert all(rec["target"] != "HKUDS/LightRAG" for rec in payload["recommendations"])


def test_gap_report_payload_accepts_custom_empty_source_project():
    payload = get_gap_report_payload(
        {
            "project": {
                "id": "proj_empty",
                "name": "Empty Project",
                "goal": "Explore a new AI/CS idea.",
                "keywords": [],
            },
            "sources": [],
        }
    )

    assert any(gap["id"] == "gap_seed_evidence" for gap in payload["gaps"])
