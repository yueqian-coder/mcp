from researchgraphos.core import (
    build_default_state,
    build_deterministic_report,
    normalize_project_state,
    report_to_context_markdown,
)


def get_projects_payload(state: dict | None = None) -> list[dict]:
    project_state = build_default_state() if state is None else normalize_project_state(state)
    project = project_state["project"]
    return [
        {
            "id": project.id,
            "name": project.name,
            "goal": project.goal,
            "keywords": list(project.keywords),
        }
    ]


def get_gap_report_payload(state: dict | None = None) -> dict:
    report = build_deterministic_report(state)
    return report.model_dump()


def get_context_markdown(state: dict | None = None) -> str:
    report = build_deterministic_report(state)
    return report_to_context_markdown(report)
