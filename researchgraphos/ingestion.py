from researchgraphos.models import ReadingStatus


KNOWN_STATUSES: set[str] = {
    "unread",
    "skimmed",
    "read",
    "noted",
    "reproduced",
    "compared",
    "rejected",
    "not_relevant",
    "later",
}


def normalize_source_status(value: str) -> ReadingStatus:
    normalized = value.strip().lower()
    if normalized in KNOWN_STATUSES:
        return normalized  # type: ignore[return-value]
    return "unread"
