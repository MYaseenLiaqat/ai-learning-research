from datetime import datetime, timedelta
from unittest.mock import patch

from app.config import settings
from app.models import AIInteraction


def _configure_llm(monkeypatch):
    monkeypatch.setattr(settings, "llm_base_url", "http://fake-llm")
    monkeypatch.setattr(settings, "llm_api_key", "fake-key")
    monkeypatch.setattr(settings, "llm_model", "fake-model")


def _mock_llm_response():
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"choices": [{"message": {"content": "AI response"}}]}

    return patch("app.routers.ai.httpx.post", return_value=FakeResponse())


def test_ai_participant_can_use_ai_on_supported_attempt(
    client, db_session, make_learner, make_task, make_attempt, monkeypatch
):
    _configure_llm(monkeypatch)
    learner = make_learner(condition="controlled_ai")
    task = make_task("supported")
    attempt = make_attempt(learner, task)

    with _mock_llm_response():
        resp = client.post(
            "/ai/chat",
            json={"attempt_id": attempt.id, "message": "help me"},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["response"] == "AI response"
    assert data["sequence_num"] == 1
    assert data["remaining_interactions"] == settings.ai_interaction_cap - 1


def test_no_ai_participant_receives_403(
    client, db_session, make_learner, make_task, make_attempt, monkeypatch
):
    _configure_llm(monkeypatch)
    learner = make_learner(condition="no_ai")
    task = make_task("supported")
    attempt = make_attempt(learner, task)

    resp = client.post(
        "/ai/chat",
        json={"attempt_id": attempt.id, "message": "help me"},
    )

    assert resp.status_code == 403


def test_ai_rejected_during_immediate(
    client, db_session, make_learner, make_task, make_attempt, monkeypatch
):
    _configure_llm(monkeypatch)
    learner = make_learner(condition="controlled_ai")
    task = make_task("immediate")
    attempt = make_attempt(learner, task)

    resp = client.post(
        "/ai/chat",
        json={"attempt_id": attempt.id, "message": "help me"},
    )

    assert resp.status_code == 403


def test_ai_rejected_during_delayed(
    client, db_session, make_learner, make_task, make_attempt, monkeypatch
):
    _configure_llm(monkeypatch)
    learner = make_learner(condition="controlled_ai")
    task = make_task("delayed")
    attempt = make_attempt(learner, task)

    resp = client.post(
        "/ai/chat",
        json={"attempt_id": attempt.id, "message": "help me"},
    )

    assert resp.status_code == 403


def test_ai_rejected_during_transfer(
    client, db_session, make_learner, make_task, make_attempt, monkeypatch
):
    _configure_llm(monkeypatch)
    learner = make_learner(condition="controlled_ai")
    task = make_task("transfer")
    attempt = make_attempt(learner, task)

    resp = client.post(
        "/ai/chat",
        json={"attempt_id": attempt.id, "message": "help me"},
    )

    assert resp.status_code == 403


def test_ai_rejected_during_criterion(
    client, db_session, make_learner, make_task, make_attempt, monkeypatch
):
    _configure_llm(monkeypatch)
    learner = make_learner(condition="controlled_ai")
    task = make_task("criterion")
    attempt = make_attempt(learner, task)

    resp = client.post(
        "/ai/chat",
        json={"attempt_id": attempt.id, "message": "help me"},
    )

    assert resp.status_code == 403


def test_future_attempt_cannot_use_ai(
    client, db_session, make_learner, make_task, make_attempt, monkeypatch
):
    _configure_llm(monkeypatch)
    learner = make_learner(condition="controlled_ai")
    task = make_task("supported")
    attempt = make_attempt(
        learner, task, scheduled_for=datetime.utcnow() + timedelta(days=1)
    )

    resp = client.post(
        "/ai/chat",
        json={"attempt_id": attempt.id, "message": "help me"},
    )

    assert resp.status_code == 409


def test_completed_attempt_cannot_use_ai(
    client, db_session, make_learner, make_task, make_attempt, monkeypatch
):
    _configure_llm(monkeypatch)
    learner = make_learner(condition="controlled_ai")
    task = make_task("supported")
    attempt = make_attempt(
        learner, task, completed_at=datetime.utcnow()
    )

    resp = client.post(
        "/ai/chat",
        json={"attempt_id": attempt.id, "message": "help me"},
    )

    assert resp.status_code == 409


def test_ai_request_cap_is_enforced(
    client, db_session, make_learner, make_task, make_attempt, monkeypatch
):
    _configure_llm(monkeypatch)
    learner = make_learner(condition="controlled_ai")
    task = make_task("supported")
    attempt = make_attempt(learner, task)

    for _ in range(settings.ai_interaction_cap):
        with _mock_llm_response():
            resp = client.post(
                "/ai/chat",
                json={"attempt_id": attempt.id, "message": "help me"},
            )
        assert resp.status_code == 200

    resp = client.post(
        "/ai/chat",
        json={"attempt_id": attempt.id, "message": "help me"},
    )
    assert resp.status_code == 429


def test_ai_interaction_is_logged(
    client, db_session, make_learner, make_task, make_attempt, monkeypatch
):
    _configure_llm(monkeypatch)
    learner = make_learner(condition="controlled_ai")
    task = make_task("supported")
    attempt = make_attempt(learner, task)

    with _mock_llm_response():
        resp = client.post(
            "/ai/chat",
            json={"attempt_id": attempt.id, "message": "help me"},
        )
    assert resp.status_code == 200

    interactions = (
        db_session.query(AIInteraction)
        .filter_by(attempt_id=attempt.id)
        .all()
    )
    assert len(interactions) == 1
    assert interactions[0].prompt == "help me"
    assert interactions[0].response == "AI response"
    assert interactions[0].sequence_num == 1