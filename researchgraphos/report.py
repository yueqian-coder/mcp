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
    sources = state.get("sources", [])
    sources_by_id = {source.id: source for source in sources}

    has_sources = bool(sources)
    has_lightrag_paper = "paper_lightrag" in sources_by_id
    has_graphrag_bench = "paper_graphrag_bench" in sources_by_id
    has_ms_graphrag = "paper_ms_graphrag" in sources_by_id
    has_lightrag_repo = "repo_lightrag" in sources_by_id
    lightrag_repo_status = sources_by_id.get("repo_lightrag").status if has_lightrag_repo else None
    lightrag_repo_done = lightrag_repo_status in {"reproduced", "compared", "not_relevant"}

    covered = []
    if has_lightrag_paper:
        source = sources_by_id["paper_lightrag"]
        covered.append(
            CoverageItem(
                source_id=source.id,
                source_title=source.title,
                learned="graph-enhanced retrieval with incremental update",
                useful_for_project="Can serve as a graph-based RAG baseline.",
                limitation_for_project="Does not provide failure-aware query routing.",
                citation=source.citation,
            )
        )
    if has_graphrag_bench:
        source = sources_by_id["paper_graphrag_bench"]
        covered.append(
            CoverageItem(
                source_id=source.id,
                source_title=source.title,
                learned="GraphRAG evaluation benchmark",
                useful_for_project="Can guide evaluation design for GraphRAG systems.",
                limitation_for_project="Does not decide when to use Vector RAG vs GraphRAG.",
                citation=source.citation,
            )
        )
    if has_ms_graphrag:
        source = sources_by_id["paper_ms_graphrag"]
        covered.append(
            CoverageItem(
                source_id=source.id,
                source_title=source.title,
                learned="graph construction and community-based retrieval",
                useful_for_project="Can serve as a strong graph retrieval baseline.",
                limitation_for_project="May be too expensive for dynamic per-query routing.",
                citation=source.citation,
            )
        )

    gaps = []
    if not has_sources:
        gaps.append(
            Gap(
                id="gap_seed_evidence",
                gap_type="concept_gap",
                missing="imported paper or repo evidence",
                reason="No sources have been imported, so the system cannot infer covered methods yet.",
                evidence="The current project state contains zero SourceItem records.",
                severity=5,
            )
        )
    gaps.extend(
        [
            Gap(
                id="gap_query_routing",
                gap_type="baseline_gap",
                missing="query routing method",
                reason=(
                    "Imported sources cover graph-based retrieval, but no source proposes a router "
                    "that selects Vector RAG, GraphRAG, Memory RAG, or Verifier per query."
                )
                if has_sources
                else (
                    "The project goal needs a routing decision, but no imported source shows a "
                    "candidate routing method."
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
        ]
    )
    if has_lightrag_repo and not lightrag_repo_done:
        gaps.append(
            Gap(
                id="gap_repro_baseline",
                gap_type="implementation_gap",
                missing="reproduced graph-based baseline",
                reason="LightRAG repo is imported but its reading status is not reproduced or compared.",
                evidence=f"Source HKUDS/LightRAG status is {lightrag_repo_status}.",
                severity=3,
            )
        )

    novelty_overlaps = []
    if has_sources:
        novelty_overlaps.extend(
            [
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
                        "Frame the novelty as project-aware research planning rather than GraphRAG "
                        "routing alone."
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
        )

    status_questions = [
        StatusQuestion(
            item="EA-GraphRAG",
            question="Have you read an adaptive GraphRAG or query routing paper such as EA-GraphRAG?",
            allowed_statuses=["unread", "skimmed", "read", "noted", "not_relevant", "later"],
        ),
        StatusQuestion(
            item="latency/token cost metric",
            question="Do you plan to include latency and token cost in the evaluation?",
            allowed_statuses=["unread", "noted", "compared", "not_relevant", "later"],
        ),
    ]
    if has_lightrag_repo and not lightrag_repo_done:
        status_questions.insert(
            1,
            StatusQuestion(
                item="HKUDS/LightRAG",
                question="Have you reproduced HKUDS/LightRAG as a graph-based baseline?",
                allowed_statuses=["noted", "reproduced", "compared", "not_relevant", "later"],
            ),
        )

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
    if not has_sources:
        recommendations.insert(
            0,
            Recommendation(
                action="import",
                target="seed paper or baseline repo",
                addresses_gap_id="gap_seed_evidence",
                reason="The project needs at least one imported source before coverage can be assessed.",
                evidence_path=EvidencePath(
                    path=[
                        "Project -has-> zero sources",
                        "zero sources -blocks-> covered method analysis",
                    ],
                    explanation="Importing a seed paper or repo creates the first evidence node.",
                    citation="Project state",
                ),
            ),
        )
    if has_lightrag_repo and not lightrag_repo_done:
        recommendations.insert(
            1,
            Recommendation(
                action="reproduce",
                target="HKUDS/LightRAG",
                addresses_gap_id="gap_repro_baseline",
                reason="Establishes a graph-based RAG baseline that can be compared against the router.",
                evidence_path=EvidencePath(
                    path=[
                        "Project -needs-> graph-based baseline",
                        "LightRAG -has_code-> HKUDS/LightRAG",
                        f"HKUDS/LightRAG -status-> {lightrag_repo_status}",
                    ],
                    explanation="The repo is known but not yet reproduced or compared.",
                    citation=sources_by_id["repo_lightrag"].citation,
                ),
            ),
        )

    if covered:
        short_answer = (
            "You have covered graph-based retrieval and GraphRAG evaluation, but the project still "
            "lacks query routing, failure detection signals, cost-aware metrics"
        )
        if has_lightrag_repo and not lightrag_repo_done:
            short_answer += ", and a reproduced graph-based baseline."
        else:
            short_answer += "."
    else:
        short_answer = (
            "No imported sources are available yet, so the project still lacks evidence for covered "
            "methods, query routing, failure detection signals, and cost-aware metrics."
        )

    return ResearchStateReport(
        project=project,
        short_answer=short_answer,
        covered=covered,
        gaps=gaps,
        novelty_overlaps=novelty_overlaps,
        status_questions=status_questions,
        recommendations=recommendations,
    )
