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

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev]"
.venv\Scripts\python -m streamlit run app/streamlit_app.py
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
```

Never commit `.env`. It is ignored by git.

## Run With Docker

```bash
docker compose up --build
```

Open `http://localhost:8501`.
