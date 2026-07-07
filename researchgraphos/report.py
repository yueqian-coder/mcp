from researchgraphos.models import (
    CoverageItem,
    EvidencePath,
    Gap,
    NoveltyOverlap,
    Recommendation,
    ResearchStateReport,
    StatusQuestion,
)


def build_research_state_report(state: dict) -> ResearchStateReport:
    project = state["project"]

    covered = [
        CoverageItem(
            source_id="paper_lightrag",
            source_title="LightRAG",
            learned="graph-enhanced retrieval with incremental update",
            useful_for_project="Can serve as a graph-based RAG baseline.",
            limitation_for_project="Does not provide failure-aware query routing.",
            citation="LightRAG paper",
        ),
        CoverageItem(
            source_id="paper_graphrag_bench",
            source_title="GraphRAG-Bench",
            learned="GraphRAG evaluation benchmark",
            useful_for_project="Can guide evaluation design for GraphRAG systems.",
            limitation_for_project="Does not decide when to use Vector RAG vs GraphRAG.",
            citation="GraphRAG-Bench paper",
        ),
        CoverageItem(
            source_id="paper_ms_graphrag",
            source_title="Microsoft GraphRAG",
            learned="graph construction and community-based retrieval",
            useful_for_project="Can serve as a strong graph retrieval baseline.",
            limitation_for_project="May be too expensive for dynamic per-query routing.",
            citation="Microsoft GraphRAG documentation or paper",
        ),
    ]

    gaps = [
        Gap(
            id="gap_query_routing",
            gap_type="baseline_gap",
            missing="query routing method",
            reason=(
                "Imported sources cover graph-based retrieval, but no source proposes a router "
                "that selects Vector RAG, GraphRAG, Memory RAG, or Verifier per query."
            ),
            evidence="No covered Method item solves query routing.",
            severity=5,
        ),
        Gap(
            id="gap_failure_signal",
            gap_type="concept_gap",
            missing="failure detection signal",
            reason="No imported source defines a signal for retrieval failure or answer failure.",
            evidence="No Concept item mentions failure detection or verifier-triggered fallback.",
            severity=4,
        ),
        Gap(
            id="gap_cost_metric",
            gap_type="metric_gap",
            missing="latency and token cost metric",
            reason="Project goal mentions reducing cost, but current coverage emphasizes retrieval quality.",
            evidence="No Metric item tracks latency or token cost.",
            severity=4,
        ),
        Gap(
            id="gap_repro_baseline",
            gap_type="implementation_gap",
            missing="reproduced graph-based baseline",
            reason="LightRAG repo is imported but its reading status is not reproduced or compared.",
            evidence="Source HKUDS/LightRAG status is noted, not reproduced.",
            severity=3,
        ),
    ]

    novelty_overlaps = [
        NoveltyOverlap(
            compared_item="EA-GraphRAG",
            similarity_points=[
                "Both consider when graph retrieval should be used.",
                "Both are related to adaptive GraphRAG routing.",
            ],
            difference_points=[
                "ResearchGraphOS uses project state and reading/reproduction status.",
                "The loop recommends research next steps, not only query-time retrieval strategy.",
            ],
            novelty_risk="medium",
            differentiation_hint=(
                "Frame the novelty as project-aware research planning rather than GraphRAG routing alone."
            ),
            citation="EA-GraphRAG paper",
        ),
        NoveltyOverlap(
            compared_item="Graphiti / Zep",
            similarity_points=["Both use graph memory to preserve context."],
            difference_points=[
                "Graphiti/Zep targets agent memory; ResearchGraphOS targets AI/CS research state."
            ],
            novelty_risk="low",
            differentiation_hint="Emphasize typed scholarly gaps and paper/repo recommendations.",
            citation="Graphiti/Zep documentation",
        ),
    ]

    status_questions = [
        StatusQuestion(
            item="EA-GraphRAG",
            question="Have you read an adaptive GraphRAG or query routing paper such as EA-GraphRAG?",
            allowed_statuses=["unread", "skimmed", "read", "noted", "not_relevant", "later"],
        ),
        StatusQuestion(
            item="HKUDS/LightRAG",
            question="Have you reproduced HKUDS/LightRAG as a graph-based baseline?",
            allowed_statuses=["noted", "reproduced", "compared", "not_relevant", "later"],
        ),
        StatusQuestion(
            item="latency/token cost metric",
            question="Do you plan to include latency and token cost in the evaluation?",
            allowed_statuses=["unread", "noted", "compared", "not_relevant", "later"],
        ),
    ]

    recommendations = [
        Recommendation(
            action="read",
            target="EA-GraphRAG",
            addresses_gap_id="gap_query_routing",
            reason="Covers the missing adaptive routing baseline.",
            evidence_path=EvidencePath(
                path=[
                    "Project -needs-> query routing",
                    "EA-GraphRAG -proposes-> adaptive graph retrieval routing",
                    "adaptive routing -addresses-> baseline gap",
                ],
                explanation="This paper is relevant because the project lacks a routing baseline.",
                citation="EA-GraphRAG paper",
            ),
        ),
        Recommendation(
            action="reproduce",
            target="HKUDS/LightRAG",
            addresses_gap_id="gap_repro_baseline",
            reason="Establishes a graph-based RAG baseline that can be compared against the router.",
            evidence_path=EvidencePath(
                path=[
                    "Project -needs-> graph-based baseline",
                    "LightRAG -has_code-> HKUDS/LightRAG",
                    "HKUDS/LightRAG -status-> noted",
                ],
                explanation="The repo is known but not yet reproduced or compared.",
                citation="HKUDS/LightRAG GitHub repository",
            ),
        ),
        Recommendation(
            action="add_metric",
            target="latency and token cost",
            addresses_gap_id="gap_cost_metric",
            reason="The project goal includes cost reduction, but the current graph lacks cost metrics.",
            evidence_path=EvidencePath(
                path=[
                    "Project goal -mentions-> reducing cost",
                    "Metric graph -missing-> latency/token cost",
                ],
                explanation="Adding these metrics makes the evaluation match the project goal.",
                citation="Project goal",
            ),
        ),
    ]

    return ResearchStateReport(
        project=project,
        short_answer=(
            "You have covered graph-based retrieval and GraphRAG evaluation, but the project still "
            "lacks query routing, failure detection signals, cost-aware metrics, and a reproduced "
            "graph-based baseline."
        ),
        covered=covered,
        gaps=gaps,
        novelty_overlaps=novelty_overlaps,
        status_questions=status_questions,
        recommendations=recommendations,
    )
