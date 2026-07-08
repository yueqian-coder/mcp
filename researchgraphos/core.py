from dataclasses import dataclass

from researchgraphos.agent import JSONProvider, ResearchStateAgent
from researchgraphos.config import LLMSettings
from researchgraphos.demo_data import build_demo_project_state
from researchgraphos.llm import OpenAICompatibleClient
from researchgraphos.models import ProjectState, ResearchStateReport
from researchgraphos.report import build_research_state_report
from researchgraphos.state import apply_source_status_overrides


DEFAULT_PROJECT_QUESTION = "What is this project missing, and what should I read or run next?"


@dataclass(frozen=True)
class AgentRunResult:
    report: ResearchStateReport
    used_fallback: bool
    fallback_reason: str = ""


def normalize_project_state(state: dict | ProjectState) -> dict:
    project_state = state if isinstance(state, ProjectState) else ProjectState.model_validate(state)
    return {
        "project": project_state.project,
        "sources": project_state.sources,
    }


def build_default_state(status_overrides: dict[str, str] | None = None) -> dict:
    state = build_demo_project_state()
    if status_overrides:
        return apply_source_status_overrides(state, status_overrides)
    return normalize_project_state(state)


def build_deterministic_report(state: dict | None = None) -> ResearchStateReport:
    project_state = build_default_state() if state is None else normalize_project_state(state)
    return build_research_state_report(project_state)


def run_research_state_agent(
    question: str,
    state: dict,
    settings: LLMSettings,
    provider: JSONProvider | None = None,
) -> AgentRunResult:
    project_state = normalize_project_state(state)
    if provider is None and not settings.is_configured:
        return AgentRunResult(
            report=build_deterministic_report(project_state),
            used_fallback=True,
            fallback_reason="API settings are incomplete",
        )

    agent_provider = provider or OpenAICompatibleClient(settings=settings)
    agent = ResearchStateAgent(provider=agent_provider)
    report = agent.answer(question=question, state=project_state)
    return AgentRunResult(
        report=report,
        used_fallback=agent.used_fallback,
        fallback_reason=_public_fallback_reason(agent.fallback_reason),
    )


def state_signature(
    state: dict,
    question: str,
    settings: LLMSettings | None = None,
) -> tuple:
    project_state = normalize_project_state(state)
    source_statuses = tuple(
        (
            source.id,
            source.title,
            source.status,
            source.citation,
        )
        for source in project_state.get("sources", [])
    )
    model_signature = ()
    if settings is not None:
        model_signature = (settings.provider, settings.model)
    return (project_state["project"].id, source_statuses, question, model_signature)


def _public_fallback_reason(reason: str) -> str:
    if not reason:
        return ""
    lower_reason = reason.lower()
    if "not configured" in lower_reason or "incomplete" in lower_reason:
        return "API settings are incomplete"
    if "validation" in lower_reason:
        return "API response failed validation"
    return "API agent failed"


def report_to_context_markdown(report: ResearchStateReport) -> str:
    lines = [
        f"# {report.project.name}",
        "",
        report.project.goal,
        "",
        "## Short Answer",
        "",
        report.short_answer,
        "",
        "## What You Have Covered",
    ]

    for item in report.covered:
        lines.extend(
            [
                "",
                f"### {item.source_title}",
                f"- Learned: {item.learned}",
                f"- Useful for project: {item.useful_for_project}",
                f"- Limitation: {item.limitation_for_project}",
                f"- Citation: {item.citation}",
            ]
        )

    lines.extend(["", "## Missing Methods / Evidence"])
    for gap in report.gaps:
        lines.extend(
            [
                "",
                f"### {gap.missing}",
                f"- Type: {gap.gap_type}",
                f"- Severity: {gap.severity}/5",
                f"- Reason: {gap.reason}",
                f"- Evidence: {gap.evidence}",
            ]
        )

    lines.extend(["", "## Novelty / Similarity Check"])
    for overlap in report.novelty_overlaps:
        lines.extend(
            [
                "",
                f"### {overlap.compared_item}",
                f"- Risk: {overlap.novelty_risk}",
                f"- Similarities: {'; '.join(overlap.similarity_points)}",
                f"- Differences: {'; '.join(overlap.difference_points)}",
                f"- Differentiation hint: {overlap.differentiation_hint}",
                f"- Citation: {overlap.citation}",
            ]
        )

    lines.extend(["", "## Recommended Next Steps"])
    for rec in report.recommendations:
        lines.extend(
            [
                "",
                f"### {rec.action}: {rec.target}",
                f"- Gap: {rec.addresses_gap_id}",
                f"- Reason: {rec.reason}",
                f"- Evidence path: {' -> '.join(rec.evidence_path.path)}",
                f"- Evidence note: {rec.evidence_path.explanation}",
            ]
        )

    return "\n".join(lines).strip() + "\n"
