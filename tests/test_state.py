from researchgraphos.demo_data import build_demo_project_state
from researchgraphos.state import apply_source_status_overrides


def test_apply_source_status_overrides_updates_matching_sources():
    state = build_demo_project_state()

    updated_state = apply_source_status_overrides(state, {"repo_lightrag": "reproduced"})

    original_repo = next(source for source in state["sources"] if source.id == "repo_lightrag")
    updated_repo = next(source for source in updated_state["sources"] if source.id == "repo_lightrag")
    assert original_repo.status == "noted"
    assert updated_repo.status == "reproduced"


def test_apply_source_status_overrides_ignores_unknown_statuses():
    state = build_demo_project_state()

    updated_state = apply_source_status_overrides(state, {"repo_lightrag": "done"})

    updated_repo = next(source for source in updated_state["sources"] if source.id == "repo_lightrag")
    assert updated_repo.status == "noted"
