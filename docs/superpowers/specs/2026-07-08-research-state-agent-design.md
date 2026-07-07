# Research State Agent Design

## Goal

Phase 2 adds an optional API-backed Research State Agent to ResearchGraphOS.

The agent takes the current project state and a project-aware question, calls an OpenAI-compatible chat API, and returns a structured `ResearchStateReport`. If no API key is configured or the API call fails, the app keeps using the deterministic demo report.

## Non-goals

- Do not build a multi-agent system.
- Do not add MCP as a primary entry point.
- Do not commit any API key or `.env` file.
- Do not replace the deterministic report fallback.
- Do not implement real PDF/arXiv/GitHub extraction in this phase.

## Configuration

Secrets live only in a local `.env` file, which is ignored by git.

Required values for agent mode:

```text
LLM_PROVIDER=openai_compatible
LLM_BASE_URL=https://example.com/v1
LLM_API_KEY=replace-with-your-key
LLM_MODEL=replace-with-model-name
```

The repository provides only `.env.example`.

## Design

New modules:

```text
researchgraphos/config.py
researchgraphos/llm.py
researchgraphos/agent.py
```

Responsibilities:

- `config.py`: load `.env` safely and construct `LLMSettings` from environment variables.
- `llm.py`: call an OpenAI-compatible `/chat/completions` endpoint and extract JSON from the assistant message.
- `agent.py`: build the research-state prompt, call an injected LLM provider, validate the JSON as `ResearchStateReport`, and fall back to deterministic report when needed.

## Agent Prompt Contract

The Research State Agent must return JSON matching the existing `ResearchStateReport` schema:

```text
project
short_answer
covered
gaps
novelty_overlaps
status_questions
recommendations
```

The prompt must tell the model:

- distinguish facts from recommendations
- avoid overclaiming novelty
- mention covered methods by source
- make missing methods specific
- attach evidence paths to recommendations

## Streamlit Behavior

The app adds an optional sidebar mode:

```text
Report mode:
- Deterministic demo report
- API Research State Agent
```

If API mode is selected without a valid API key, the app shows a warning and uses deterministic fallback.

## Safety

The app never displays API keys.

The app never stores API keys.

`.env` remains ignored by git.
