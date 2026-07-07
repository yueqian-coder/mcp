from typing import get_args

from researchgraphos.models import ReadingStatus


VALID_READING_STATUSES = set(get_args(ReadingStatus))


def apply_source_status_overrides(state: dict, overrides: dict[str, str]) -> dict:
    """Return a state copy with valid SourceItem status overrides applied."""
    updated_state = dict(state)
    updated_sources = []
    for source in state.get("sources", []):
        override = overrides.get(source.id)
        if override in VALID_READING_STATUSES and override != source.status:
            updated_sources.append(source.model_copy(update={"status": override}))
        else:
            updated_sources.append(source)
    updated_state["sources"] = updated_sources
    return updated_state
