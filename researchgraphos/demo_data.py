from researchgraphos.models import Project, SourceItem


def build_demo_project_state() -> dict:
    project = Project(
        id="proj_graphrag_router",
        name="Failure-aware GraphRAG Router",
        goal="Decide when to use Vector RAG, GraphRAG, Memory RAG, or Verifier.",
        keywords=["GraphRAG", "query routing", "RAG evaluation", "cost-aware retrieval"],
    )

    sources = [
        SourceItem(
            id="paper_lightrag",
            title="LightRAG",
            kind="paper",
            status="read",
            citation="LightRAG paper",
        ),
        SourceItem(
            id="paper_graphrag_bench",
            title="GraphRAG-Bench",
            kind="paper",
            status="read",
            citation="GraphRAG-Bench paper",
        ),
        SourceItem(
            id="paper_ms_graphrag",
            title="Microsoft GraphRAG",
            kind="paper",
            status="skimmed",
            citation="Microsoft GraphRAG documentation or paper",
        ),
        SourceItem(
            id="repo_lightrag",
            title="HKUDS/LightRAG",
            kind="repo",
            status="noted",
            citation="HKUDS/LightRAG GitHub repository",
        ),
    ]

    return {"project": project, "sources": sources}
