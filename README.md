# ResearchGraphOS

A self-hosted project-aware research graph engine for AI/CS literature review.

Core loop:

```text
Ask -> Diagnose Gap -> Confirm Status -> Recommend Next Step
```

Architecture target:

```text
Core Engine -> Web App
            -> future MCP bridge
```

The current app keeps reusable product logic in `researchgraphos/` so the web UI and a
future MCP server can share the same project state, gap report, and context export logic.

This MVP starts with a curated GraphRAG Router demo and generates a Detailed Research State Report.

## MVP

This MVP starts with a curated GraphRAG Router demo and generates a Detailed Research State Report:

- What You Have Covered
- Missing Methods / Evidence
- Novelty / Similarity Check
- Status Check
- Recommended Next Steps

## Run Locally

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev]"
.venv\Scripts\python -m streamlit run app/streamlit_app.py
```

macOS/Linux:

```bash
python -m venv .venv
./.venv/bin/python -m pip install -e ".[dev]"
./.venv/bin/python -m streamlit run app/streamlit_app.py
```

Open `http://localhost:8501`.

## Optional API Research State Agent

The app works without an API key by using the deterministic demo report.

To enable the API-backed Research State Agent:

```bash
copy .env.example .env
```

Then edit `.env`:

```text
LLM_PROVIDER=openai_compatible
LLM_BASE_URL=https://your-provider.example/v1
LLM_API_KEY=replace-with-your-key
LLM_MODEL=replace-with-model-name
LLM_ALLOW_INSECURE_BASE_URL=false
```

Never commit `.env`. It is ignored by git.

API mode calls the model only when you click **Generate API report**. If the API call fails
or returns invalid JSON, the app shows a warning and falls back to the deterministic report.

## Codex / Claude Context

The core package can export a project report as Markdown context for tools such as Codex
or Claude. A real MCP server is not exposed yet; the current `researchgraphos.mcp_bridge`
module is a read-only foundation for future MCP tools.

Quick smoke:

```powershell
.venv\Scripts\python -c "from researchgraphos.mcp_bridge import get_context_markdown; print(get_context_markdown()[:200])"
```

Current bridge functions:

- `get_projects_payload()`
- `get_gap_report_payload()`
- `get_context_markdown()`

These are read-only Python functions, not an MCP transport server yet.

## Run With Docker

```bash
docker compose up --build
```

Open `http://localhost:8501`.

Docker Compose reads the same environment variables from your shell or local `.env` file and
passes them into the container. The `.env` file is not copied into the image.
