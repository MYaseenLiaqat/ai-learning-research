"""Regression: the application default AI interaction cap must be 8."""

from app.config import Settings


def test_default_ai_interaction_cap_is_8_without_env_override(monkeypatch):
    """Without .env or AI_INTERACTION_CAP, the cap must default to 8."""
    monkeypatch.delenv("AI_INTERACTION_CAP", raising=False)
    settings = Settings(_env_file=None)
    assert settings.ai_interaction_cap == 8