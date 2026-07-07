from researchgraphos.models import Project, SourceItem


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
