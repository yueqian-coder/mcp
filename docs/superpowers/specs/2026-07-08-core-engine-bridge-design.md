# Core Engine Bridge Design

## Goal

Start building ResearchGraphOS toward the final architecture:

```text
Core Engine + Web App + MCP bridge
```

This phase creates a small core API that the Streamlit web app can use now and a future
MCP server can wrap later.

## Agreed Architecture

ResearchGraphOS should not put product logic inside Streamlit. The core package owns
project state, report generation, API-agent fallback, and context export.

```text
researchgraphos core
  -> Web App
  -> future MCP server
  -> future CLI/export tools
```

## Scope

Build the first core-engine slice:

- Create a reusable core module for default project state and report generation.
- Create a context export function for Codex, Claude, and future MCP tools.
- Create a lightweight MCP bridge module without adding an MCP dependency yet.
- Update Streamlit to call the core module instead of owning the application flow.

## Non-goals

- Do not implement a real MCP server in this phase.
- Do not add PDF, arXiv, GitHub, or arbitrary URL import.
- Do not add graph/vector storage.
- Do not add a second UI.
- Do not remove the deterministic fallback report.

## Interfaces

Core module:

```text
build_default_state(status_overrides=None) -> dict
build_deterministic_report(state=None) -> ResearchStateReport
run_research_state_agent(question, state, settings, provider=None) -> AgentRunResult
report_to_context_markdown(report) -> str
state_signature(state, question, settings=None) -> tuple
```

MCP bridge module:

```text
get_projects_payload(state=None) -> list[dict]
get_gap_report_payload(state=None) -> dict
get_context_markdown(state=None) -> str
```

These bridge functions must be dependency-light and JSON-serializable so a future MCP server
can expose them as tools.

## Testing

Tests must prove:

- Core applies source status overrides before building reports.
- Core can export a context markdown file for Codex/Claude.
- API agent runner reports fallback status without raising when no provider is configured.
- MCP bridge payloads are JSON-serializable and include gaps/recommendations.
- Streamlit can import the shared core functions.

## Safety

- MCP bridge is read-only in this phase.
- No API key is included in exported context.
- API errors still use deterministic fallback.
- Future write tools such as `add_source` and `update_status` are explicitly out of scope.
