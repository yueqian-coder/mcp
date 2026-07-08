# Core Engine Bridge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a reusable ResearchGraphOS core layer that both the Streamlit web app and a future MCP server can call.

**Architecture:** Move project-state setup, report generation, API-agent fallback, cache signatures, and context export into `researchgraphos/core.py`. Add `researchgraphos/mcp_bridge.py` as a dependency-light read-only wrapper for future MCP tools. Keep Streamlit as a thin UI.

**Tech Stack:** Python 3.12, Pydantic, Streamlit, pytest. No MCP dependency in this phase.

## Global Constraints

- Web is the main user experience.
- MCP bridge is read-only in this phase.
- Core logic lives in `researchgraphos/`, not in Streamlit.
- Deterministic report remains the fallback.
- No PDF, arXiv, GitHub, URL fetching, graph database, vector database, or MCP server implementation.
- No real API calls in tests.

---

### Task 1: Core Engine API

**Files:**
- Create: `researchgraphos/core.py`
- Test: `tests/test_core.py`

**Interfaces:**
- Produces: `build_default_state(status_overrides: dict[str, str] | None = None) -> dict`
- Produces: `build_deterministic_report(state: dict | None = None) -> ResearchStateReport`
- Produces: `run_research_state_agent(question: str, state: dict, settings: LLMSettings, provider: JSONProvider | None = None) -> AgentRunResult`
- Produces: `report_to_context_markdown(report: ResearchStateReport) -> str`
- Produces: `state_signature(state: dict, question: str, settings: LLMSettings | None = None) -> tuple`

- [ ] Write failing tests for status override, context export, and API fallback result.
- [ ] Run targeted tests and confirm they fail because `researchgraphos.core` does not exist.
- [ ] Implement the minimal core API.
- [ ] Run targeted tests and confirm they pass.

### Task 2: MCP Bridge Wrapper

**Files:**
- Create: `researchgraphos/mcp_bridge.py`
- Test: `tests/test_mcp_bridge.py`

**Interfaces:**
- Consumes: `build_default_state`
- Consumes: `build_deterministic_report`
- Consumes: `report_to_context_markdown`
- Produces: `get_projects_payload(state: dict | None = None) -> list[dict]`
- Produces: `get_gap_report_payload(state: dict | None = None) -> dict`
- Produces: `get_context_markdown(state: dict | None = None) -> str`

- [ ] Write failing tests for JSON-serializable project and report payloads.
- [ ] Run targeted tests and confirm they fail because `researchgraphos.mcp_bridge` does not exist.
- [ ] Implement read-only bridge functions.
- [ ] Run targeted tests and confirm they pass.

### Task 3: Thin Streamlit UI

**Files:**
- Modify: `app/streamlit_app.py`
- Test: existing tests plus `py_compile`

**Interfaces:**
- Consumes: `DEFAULT_PROJECT_QUESTION`
- Consumes: `build_default_state`
- Consumes: `build_deterministic_report`
- Consumes: `run_research_state_agent`
- Consumes: `state_signature`

- [ ] Replace local Streamlit application flow with core API calls.
- [ ] Keep UI behavior unchanged for deterministic and API modes.
- [ ] Run tests, ruff, py_compile, wheel build, key scan, and localhost smoke.
