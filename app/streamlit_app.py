import streamlit as st

from researchgraphos.agent import ResearchStateAgent
from researchgraphos.config import LLMSettings, load_env_file
from researchgraphos.demo_data import build_demo_project_state
from researchgraphos.llm import OpenAICompatibleClient
from researchgraphos.report import build_research_state_report


st.set_page_config(page_title="ResearchGraphOS", layout="wide")

load_env_file()
state = build_demo_project_state()
settings = LLMSettings.from_env()

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

if report_mode == "API Research State Agent":
    if settings.is_configured:
        provider = OpenAICompatibleClient(settings=settings)
        report = ResearchStateAgent(provider=provider).answer(question=question, state=state)
        st.sidebar.success("API agent mode enabled.")
    else:
        report = build_research_state_report(state)
        st.sidebar.warning("API settings are incomplete. Using deterministic fallback.")
else:
    report = build_research_state_report(state)

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
for question in report.status_questions:
    st.write(question.question)
    st.selectbox(
        label=f"Status for {question.item}",
        options=question.allowed_statuses,
        key=f"status_{question.item}",
    )

st.subheader("Recommended Next Steps")
for rec in report.recommendations:
    with st.expander(f"{rec.action}: {rec.target}", expanded=True):
        st.write(rec.reason)
        st.markdown("**Evidence Path**")
        for step in rec.evidence_path.path:
            st.write(f"- {step}")
        st.caption(rec.evidence_path.explanation)
