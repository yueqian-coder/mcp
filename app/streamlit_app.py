from typing import get_args

import streamlit as st

from researchgraphos.agent import ResearchStateAgent
from researchgraphos.config import LLMSettings, load_env_file
from researchgraphos.demo_data import build_demo_project_state
from researchgraphos.llm import OpenAICompatibleClient
from researchgraphos.models import ReadingStatus, ResearchStateReport
from researchgraphos.report import build_research_state_report
from researchgraphos.state import apply_source_status_overrides


st.set_page_config(page_title="ResearchGraphOS", layout="wide")

load_env_file()
base_state = build_demo_project_state()
settings = LLMSettings.from_env()
reading_status_options = list(get_args(ReadingStatus))


def state_signature(state: dict, question: str) -> tuple:
    source_statuses = tuple((source.id, source.status) for source in state.get("sources", []))
    return (state["project"].id, source_statuses, question)


def cached_api_report(signature: tuple) -> ResearchStateReport | None:
    if st.session_state.get("api_report_signature") != signature:
        return None
    payload = st.session_state.get("api_report")
    if not payload:
        return None
    return ResearchStateReport.model_validate(payload)


st.title("ResearchGraphOS")
st.caption("Ask -> Diagnose Gap -> Confirm Status -> Recommend Next Step")

with st.sidebar:
    st.header("Report Mode")
    report_mode = st.radio(
        "Choose how to generate the report",
        options=["Deterministic demo report", "API Research State Agent"],
    )
    question = st.text_area(
        "Project-aware question",
        value="What is this project missing, and what should I read or run next?",
        height=120,
    )
    st.divider()
    st.header("Source Status")
    status_overrides = {}
    for source in base_state["sources"]:
        status_overrides[source.id] = st.selectbox(
            source.title,
            options=reading_status_options,
            index=reading_status_options.index(source.status),
            key=f"source_status_{source.id}",
        )

state = apply_source_status_overrides(base_state, status_overrides)
deterministic_report = build_research_state_report(state)
signature = state_signature(state, question)
report = deterministic_report

if report_mode == "API Research State Agent":
    cached_report = cached_api_report(signature)
    if cached_report is not None:
        report = cached_report
        st.sidebar.caption("Using the last API report for this question and source state.")

    if st.sidebar.button("Generate API report", type="primary", use_container_width=True):
        report = deterministic_report
        st.session_state.pop("api_report", None)
        st.session_state.pop("api_report_signature", None)
        if settings.is_configured:
            provider = OpenAICompatibleClient(settings=settings)
            agent = ResearchStateAgent(provider=provider)
            report = agent.answer(question=question, state=state)
            if agent.used_fallback:
                st.sidebar.warning(
                    f"API agent failed; using deterministic fallback. Reason: {agent.fallback_reason}"
                )
            else:
                st.session_state["api_report"] = report.model_dump()
                st.session_state["api_report_signature"] = signature
                st.sidebar.success("API report generated.")
        else:
            st.sidebar.warning("API settings are incomplete. Using deterministic fallback.")
else:
    st.session_state.pop("api_report", None)
    st.session_state.pop("api_report_signature", None)

if report_mode == "API Research State Agent" and settings.is_configured:
    if not st.session_state.get("api_report") and report == deterministic_report:
        st.sidebar.caption("Click Generate API report to call the configured model.")

st.header(report.project.name)
st.write(report.project.goal)

st.subheader("Short Answer")
st.write(report.short_answer)

st.subheader("What You Have Covered")
for item in report.covered:
    with st.expander(item.source_title, expanded=True):
        st.markdown(f"**Learned:** {item.learned}")
        st.markdown(f"**Useful for project:** {item.useful_for_project}")
        st.markdown(f"**Limitation:** {item.limitation_for_project}")
        st.caption(f"Citation: {item.citation}")

st.subheader("Missing Methods / Evidence")
for gap in report.gaps:
    st.markdown(f"**{gap.missing}** ({gap.gap_type}, severity {gap.severity}/5)")
    st.write(gap.reason)
    st.caption(f"Evidence: {gap.evidence}")

st.subheader("Novelty / Similarity Check")
for overlap in report.novelty_overlaps:
    with st.expander(f"{overlap.compared_item} - risk: {overlap.novelty_risk}", expanded=True):
        st.markdown("**Similarities**")
        for point in overlap.similarity_points:
            st.write(f"- {point}")
        st.markdown("**Differences**")
        for point in overlap.difference_points:
            st.write(f"- {point}")
        st.markdown(f"**Differentiation hint:** {overlap.differentiation_hint}")
        st.caption(f"Citation: {overlap.citation}")

st.subheader("Status Check")
for status_question in report.status_questions:
    st.write(status_question.question)
    st.selectbox(
        label=f"Status for {status_question.item}",
        options=status_question.allowed_statuses,
        key=f"status_{status_question.item}",
    )

st.subheader("Recommended Next Steps")
for rec in report.recommendations:
    with st.expander(f"{rec.action}: {rec.target}", expanded=True):
        st.write(rec.reason)
        st.markdown("**Evidence Path**")
        for step in rec.evidence_path.path:
            st.write(f"- {step}")
        st.caption(rec.evidence_path.explanation)
