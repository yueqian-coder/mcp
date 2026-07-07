from researchgraphos.agent import ResearchStateAgent
from researchgraphos.demo_data import build_demo_project_state
from researchgraphos.report import build_research_state_report


class FakeProvider:
    def __init__(self, payload):
        self.payload = payload
        self.messages = []

    def complete_json(self, messages):
        self.messages = messages
        return self.payload


class FailingProvider:
    def complete_json(self, messages):
        raise RuntimeError("network unavailable")


def test_research_state_agent_validates_provider_json():
    state = build_demo_project_state()
    payload = build_research_state_report(state).model_dump()
    provider = FakeProvider(payload)
    agent = ResearchStateAgent(provider=provider)

    report = agent.answer("What am I missing?", state)

    assert report.project.name == "Failure-aware GraphRAG Router"
    assert any(gap.missing == "query routing method" for gap in report.gaps)
    assert "What am I missing?" in provider.messages[-1]["content"]
    assert not agent.used_fallback
    assert agent.fallback_reason == ""


def test_research_state_agent_falls_back_to_deterministic_report():
    state = build_demo_project_state()
    agent = ResearchStateAgent(provider=FailingProvider())

    report = agent.answer("What am I missing?", state)

    assert report.short_answer == build_research_state_report(state).short_answer
    assert any(rec.target == "EA-GraphRAG" for rec in report.recommendations)
    assert agent.used_fallback
    assert "network unavailable" in agent.fallback_reason
