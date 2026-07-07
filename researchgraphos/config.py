import os
from dataclasses import dataclass
from pathlib import Path


def load_env_file(path: str = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


@dataclass(frozen=True)
class LLMSettings:
    provider: str
    base_url: str
    api_key: str
    model: str
    allow_insecure_base_url: bool = False

    @classmethod
    def from_env(cls) -> "LLMSettings":
        return cls(
            provider=os.getenv("LLM_PROVIDER", "openai_compatible"),
            base_url=os.getenv("LLM_BASE_URL", ""),
            api_key=os.getenv("LLM_API_KEY", ""),
            model=os.getenv("LLM_MODEL", ""),
            allow_insecure_base_url=os.getenv("LLM_ALLOW_INSECURE_BASE_URL", "")
            .strip()
            .lower()
            in {"1", "true", "yes", "on"},
        )

    @property
    def is_configured(self) -> bool:
        return bool(
            self.provider == "openai_compatible"
            and self.base_url.strip()
            and self.api_key.strip()
            and self.model.strip()
        )
