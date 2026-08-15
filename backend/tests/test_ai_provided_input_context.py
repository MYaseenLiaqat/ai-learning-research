"""Tests for the AI request context for exec_result tasks."""

from datetime import datetime
from unittest.mock import patch

from app.config import settings
from app.models import Task


def _configure_llm(monkeypatch):
    monkeypatch.setattr(settings, "llm_base_url", "http://fake-llm")
    monkeypatch.setattr(settings, "llm_api_key", "fake-key")
    monkeypatch.setattr(settings, "llm_model", "fake-model")


def test_ai_context_lists_provided_input_and_prohibits_redefinition(
    client, db_session, make_learner, make_attempt, concept, monkeypatch
):
    _configure_llm(monkeypatch)
    task = Task(
        concept_id=concept.id,
        type="supported",
        prompt_text="Count temperatures above 30.",
        grading_spec={
            "mode": "exec_result",
            "result_var": "result",
            "tests": [
                {"inputs": {"temperatures": []}, "expected": 0},
                {"inputs": {"temperatures": [31]}, "expected": 1},
            ],
        },
        scheduled_offset_days=0,
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    learner = make_learner(condition="controlled_ai")
    attempt = make_attempt(learner, task, started_at=datetime.utcnow())
    captured = {}

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"choices": [{"message": {"content": "AI response"}}]}

    def fake_post(url, headers=None, json=None, timeout=None):
        captured["body"] = json
        return FakeResponse()

    with patch("app.routers.ai.httpx.post", side_effect=fake_post):
        resp = client.post(
            "/ai/chat",
            json={"attempt_id": attempt.id, "message": "help me"},
        )

    assert resp.status_code == 200
    user_content = captured["body"]["messages"][1]["content"]
    assert "temperatures" in user_content
    assert "Never assign to, redefine, replace, or recreate them" in user_content
    assert "final answer to `result`" in user_content