import json

from researchgraphos.config import LLMSettings
from researchgraphos.llm import OpenAICompatibleClient


class FakeTransport:
    def __init__(self):
        self.calls = []

    def __call__(self, url, headers, payload, timeout):
        self.calls.append(
            {
                "url": url,
                "headers": headers,
                "payload": payload,
                "timeout": timeout,
            }
        )
        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps({"ok": True, "items": [1, 2, 3]}),
                    }
                }
            ]
        }


def test_openai_compatible_client_posts_chat_completion_and_extracts_json():
    transport = FakeTransport()
    settings = LLMSettings(
        provider="openai_compatible",
        base_url="https://example.test/v1",
        api_key="test-key",
        model="test-model",
    )
    client = OpenAICompatibleClient(settings=settings, transport=transport)

    result = client.complete_json([{"role": "user", "content": "Return JSON"}])

    assert result == {"ok": True, "items": [1, 2, 3]}
    assert transport.calls[0]["url"] == "https://example.test/v1/chat/completions"
    assert transport.calls[0]["headers"]["Authorization"] == "Bearer test-key"
    assert transport.calls[0]["payload"]["model"] == "test-model"
    assert transport.calls[0]["payload"]["messages"][0]["content"] == "Return JSON"


def test_openai_compatible_client_strips_markdown_json_fence():
    def transport(url, headers, payload, timeout):
        return {
            "choices": [
                {
                    "message": {
                        "content": "```json\n{\"ok\": true}\n```",
                    }
                }
            ]
        }

    settings = LLMSettings(
        provider="openai_compatible",
        base_url="https://example.test/v1/",
        api_key="test-key",
        model="test-model",
    )
    client = OpenAICompatibleClient(settings=settings, transport=transport)

    assert client.complete_json([{"role": "user", "content": "Return JSON"}]) == {"ok": True}
