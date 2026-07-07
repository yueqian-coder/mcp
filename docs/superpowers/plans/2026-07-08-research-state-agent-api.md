# Research State Agent API Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an optional OpenAI-compatible Research State Agent that generates `ResearchStateReport` JSON from project state and falls back to deterministic output when API mode is unavailable.

**Architecture:** Keep the existing deterministic report as the stable baseline. Add configuration, a tiny OpenAI-compatible client, and an agent wrapper with dependency injection so tests use fake providers and never call the network.

**Tech Stack:** Python 3.12, pytest, pydantic, Streamlit, standard-library `urllib.request`. No secret values committed.

## Global Constraints

- `.env` is local-only and ignored by git.
- `.env.example` contains placeholders only.
- No real API calls in tests.
- Agent mode is optional in the UI.
- Deterministic report remains the fallback.

---

### Task 1: Configuration

**Files:**
- Create: `researchgraphos/config.py`
- Create: `.env.example`
- Test: `tests/test_config.py`

**Interfaces:**
- Produces: `LLMSettings.from_env() -> LLMSettings`
- Produces: `load_env_file(path: str = ".env") -> None`

### Task 2: OpenAI-Compatible Client

**Files:**
- Create: `researchgraphos/llm.py`
- Test: `tests/test_llm.py`

**Interfaces:**
- Produces: `OpenAICompatibleClient.complete_json(messages: list[dict[str, str]]) -> dict`

### Task 3: Research State Agent

**Files:**
- Create: `researchgraphos/agent.py`
- Test: `tests/test_agent.py`

**Interfaces:**
- Produces: `ResearchStateAgent.answer(question: str, state: dict) -> ResearchStateReport`

### Task 4: Streamlit Agent Mode

**Files:**
- Modify: `app/streamlit_app.py`
- Modify: `README.md`

**Interfaces:**
- Consumes: `LLMSettings.from_env`
- Consumes: `OpenAICompatibleClient`
- Consumes: `ResearchStateAgent`

### Task 5: Verification

Run:

```bash
.venv\Scripts\python -m pytest -q
.venv\Scripts\python -m ruff check .
.venv\Scripts\python -m py_compile app/streamlit_app.py researchgraphos\*.py
```

Expected:

```text
all tests pass
All checks passed!
py_compile exits 0
```

Then push to `origin/main`.
