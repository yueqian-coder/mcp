from researchgraphos.models import Project, SourceItem
from researchgraphos.demo_data import build_demo_project_state
from researchgraphos.report import build_research_state_report


def test_project_and_source_models_can_be_created():
    project = Project(
        id="proj_graphrag_router",
        name="Failure-aware GraphRAG Router",
        goal="Decide when to use Vector RAG, GraphRAG, Memory RAG, or Verifier.",
        keywords=["GraphRAG", "routing", "RAG evaluation"],
    )
    source = SourceItem(
        id="paper_lightrag",
        title="LightRAG",
        kind="paper",
        status="read",
        citation="LightRAG paper",
    )

    assert project.name == "Failure-aware GraphRAG Router"
    assert source.kind == "paper"
    assert source.status == "read"


def test_demo_project_state_contains_graphrag_sources():
    state = build_demo_project_state()

    assert state["project"].name == "Failure-aware GraphRAG Router"
    assert len(state["sources"]) >= 4
    assert any(source.title == "LightRAG" for source in state["sources"])
    assert any(source.kind == "repo" for source in state["sources"])


def test_report_includes_covered_missing_novelty_and_recommendations():
    state = build_demo_project_state()
    report = build_research_state_report(state)

    assert "query routing" in report.short_answer.lower()
    assert any("graph-enhanced retrieval" in item.learned for item in report.covered)
    assert any(gap.missing == "query routing method" for gap in report.gaps)
    assert any(overlap.compared_item == "EA-GraphRAG" for overlap in report.novelty_overlaps)
    assert any("Have you read" in question.question for question in report.status_questions)
    assert any(rec.target == "EA-GraphRAG" for rec in report.recommendations)
    assert all(rec.evidence_path.path for rec in report.recommendations)
