from researchgraphos.demo_data import build_demo_project_state
from researchgraphos.models import EvidencePath, Project, Recommendation, ResearchStateReport, SourceItem
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


def test_report_does_not_claim_specific_coverage_without_sources():
    state = {
        "project": Project(
            id="empty_project",
            name="Empty Project",
            goal="Explore a new AI/CS idea.",
            keywords=[],
        ),
        "sources": [],
    }

    report = build_research_state_report(state)

    assert report.covered == []
    assert "LightRAG" not in report.short_answer
    assert all(item.source_title != "LightRAG" for item in report.covered)


def test_report_does_not_recommend_reproducing_repo_that_is_already_reproduced():
    state = build_demo_project_state()
    updated_sources = []
    for source in state["sources"]:
        if source.id == "repo_lightrag":
            source = source.model_copy(update={"status": "reproduced"})
        updated_sources.append(source)
    state["sources"] = updated_sources

    report = build_research_state_report(state)

    assert all(gap.id != "gap_repro_baseline" for gap in report.gaps)
    assert all(rec.target != "HKUDS/LightRAG" for rec in report.recommendations)


def test_research_state_report_rejects_recommendation_for_missing_gap():
    project = Project(id="proj", name="Project", goal="Goal", keywords=[])

    try:
        ResearchStateReport(
            project=project,
            short_answer="answer",
            covered=[],
            gaps=[],
            novelty_overlaps=[],
            status_questions=[],
            recommendations=[
                Recommendation(
                    action="read",
                    target="Missing Paper",
                    addresses_gap_id="missing_gap",
                    reason="reason",
                    evidence_path=EvidencePath(
                        path=["Project -needs-> missing thing"],
                        explanation="explanation",
                        citation="citation",
                    ),
                )
            ],
        )
    except ValueError as exc:
        assert "missing_gap" in str(exc)
    else:
        raise AssertionError("Expected report validation to reject missing gap reference")
