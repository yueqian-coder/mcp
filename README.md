# ResearchGraphOS

A self-hosted project-aware research graph engine for AI/CS literature review.

Core loop:

```text
Ask -> Diagnose Gap -> Confirm Status -> Recommend Next Step
```

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

## Run With Docker

```bash
docker compose up --build
```

Open `http://localhost:8501`.

Docker Compose reads the same environment variables from your shell or local `.env` file and
passes them into the container. The `.env` file is not copied into the image.
