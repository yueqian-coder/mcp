from pathlib import Path

from researchgraphos.config import LLMSettings, load_env_file


def test_llm_settings_reads_openai_compatible_env(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai_compatible")
    monkeypatch.setenv("LLM_BASE_URL", "https://example.test/v1")
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    monkeypatch.setenv("LLM_MODEL", "test-model")

    settings = LLMSettings.from_env()

    assert settings.provider == "openai_compatible"
    assert settings.base_url == "https://example.test/v1"
    assert settings.api_key == "test-key"
    assert settings.model == "test-model"
    assert settings.is_configured


def test_llm_settings_reports_unconfigured_without_key(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai_compatible")
    monkeypatch.setenv("LLM_BASE_URL", "https://example.test/v1")
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.setenv("LLM_MODEL", "test-model")

    settings = LLMSettings.from_env()

    assert not settings.is_configured


def test_load_env_file_sets_missing_values(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("LLM_MODEL=env-file-model\nLLM_API_KEY=env-file-key\n", encoding="utf-8")
    monkeypatch.delenv("LLM_MODEL", raising=False)
    monkeypatch.setenv("LLM_API_KEY", "existing-key")

    load_env_file(str(env_file))

    assert LLMSettings.from_env().model == "env-file-model"
    assert LLMSettings.from_env().api_key == "existing-key"
    assert Path(env_file).exists()
