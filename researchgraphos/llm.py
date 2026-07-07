import json
import urllib.error
import urllib.request
from collections.abc import Callable
from typing import Any

from researchgraphos.config import LLMSettings


Transport = Callable[[str, dict[str, str], dict[str, Any], float], dict[str, Any]]


class LLMError(RuntimeError):
    """Raised when an LLM call fails or returns invalid data."""


def _default_transport(
    url: str,
    headers: dict[str, str],
    payload: dict[str, Any],
    timeout: float,
) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise LLMError(f"LLM request failed: {exc}") from exc


def _extract_json_text(content: str) -> str:
    text = content.strip()
    if text.startswith("```json"):
        text = text.removeprefix("```json").strip()
    elif text.startswith("```"):
        text = text.removeprefix("```").strip()
    if text.endswith("```"):
        text = text.removesuffix("```").strip()
    return text


class OpenAICompatibleClient:
    def __init__(
        self,
        settings: LLMSettings,
        transport: Transport = _default_transport,
        timeout: float = 60.0,
    ):
        self.settings = settings
        self.transport = transport
        self.timeout = timeout

    def complete_json(self, messages: list[dict[str, str]]) -> dict[str, Any]:
        if not self.settings.is_configured:
            raise LLMError("LLM settings are not configured")

        url = f"{self.settings.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.settings.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.settings.model,
            "messages": messages,
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
        }
        response = self.transport(url, headers, payload, self.timeout)
        try:
            content = response["choices"][0]["message"]["content"]
            return json.loads(_extract_json_text(content))
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise LLMError(f"LLM response did not contain valid JSON: {exc}") from exc
