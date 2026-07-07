from researchgraphos.ingestion import normalize_source_status


def test_normalize_source_status_accepts_known_statuses():
    assert normalize_source_status("read") == "read"
    assert normalize_source_status("reproduced") == "reproduced"


def test_normalize_source_status_defaults_unknown_to_unread():
    assert normalize_source_status("") == "unread"
    assert normalize_source_status("finished") == "unread"
