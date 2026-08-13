from datetime import datetime, timedelta
from unittest.mock import patch

from app.config import settings


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


def test_explicit_start_sets_started_at(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner(condition="controlled_ai")
    task = make_task("supported")
    attempt = make_attempt(learner, task)

    resp = client.post(f"/learning/loops/start?learner_id={learner.id}")

    assert resp.status_code == 200
    data = resp.json()
    assert data["started_at"] is not None
    assert data["expires_at"] is not None
    assert data["module_version"] == "v0.2.0"

    db_session.refresh(attempt)
    assert attempt.started_at is not None


def test_explicit_start_stores_module_version_v020(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner(condition="controlled_ai")
    task = make_task("supported")
    attempt = make_attempt(learner, task)

    client.post(f"/learning/loops/start?learner_id={learner.id}")

    db_session.refresh(attempt)
    assert attempt.module_version == "v0.2.0"


def test_second_explicit_start_does_not_reset(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner(condition="controlled_ai")
    task = make_task("supported")
    attempt = make_attempt(learner, task)

    first = client.post(f"/learning/loops/start?learner_id={learner.id}")
    first_started = first.json()["started_at"]

    second = client.post(f"/learning/loops/start?learner_id={learner.id}")
    second_started = second.json()["started_at"]

    assert first_started == second_started


def test_ai_rejected_before_explicit_start(
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

    assert resp.status_code == 409


def test_supported_submission_rejected_before_explicit_start(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    task = make_task("supported")
    attempt = make_attempt(learner, task)

    resp = client.post(
        f"/tasks/{task.id}/submit",
        params={"learner_id": learner.id},
        json={"code": "result = 0\n"},
    )

    assert resp.status_code == 409


def test_ai_allowed_during_active_session(
    client, db_session, make_learner, make_task, make_attempt, monkeypatch
):
    _configure_llm(monkeypatch)
    learner = make_learner(condition="controlled_ai")
    task = make_task("supported")
    attempt = make_attempt(learner, task, started_at=datetime.utcnow())

    with _mock_llm_response():
        resp = client.post(
            "/ai/chat",
            json={"attempt_id": attempt.id, "message": "help me"},
        )

    assert resp.status_code == 200


def test_no_ai_remains_blocked(
    client, db_session, make_learner, make_task, make_attempt, monkeypatch
):
    _configure_llm(monkeypatch)
    learner = make_learner(condition="no_ai")
    task = make_task("supported")
    attempt = make_attempt(learner, task, started_at=datetime.utcnow())

    with _mock_llm_response():
        resp = client.post(
            "/ai/chat",
            json={"attempt_id": attempt.id, "message": "help me"},
        )

    assert resp.status_code == 403


def test_ai_rejected_after_expiry(
    client, db_session, make_learner, make_task, make_attempt, monkeypatch
):
    _configure_llm(monkeypatch)
    learner = make_learner(condition="controlled_ai")
    task = make_task("supported")
    # Session started 21 minutes ago (> 20 min limit).
    attempt = make_attempt(
        learner,
        task,
        started_at=datetime.utcnow() - timedelta(minutes=21),
    )

    with _mock_llm_response():
        resp = client.post(
            "/ai/chat",
            json={"attempt_id": attempt.id, "message": "help me"},
        )

    assert resp.status_code == 409


def test_supported_submission_rejected_after_expiry(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    task = make_task("supported")
    # Session started 21 minutes ago (> 20 min limit).
    attempt = make_attempt(
        learner,
        task,
        started_at=datetime.utcnow() - timedelta(minutes=21),
    )

    resp = client.post(
        f"/tasks/{task.id}/submit",
        params={"learner_id": learner.id},
        json={"code": "result = 0\n"},
    )

    assert resp.status_code == 409


def test_ai_budget_is_attempt_scoped(
    client, db_session, make_learner, make_task, make_attempt, monkeypatch
):
    _configure_llm(monkeypatch)
    learner = make_learner(condition="controlled_ai")

    # Two separate supported attempts.
    task1 = make_task("supported")
    task2 = make_task("supported")
    attempt1 = make_attempt(learner, task1, started_at=datetime.utcnow())
    attempt2 = make_attempt(learner, task2, started_at=datetime.utcnow())

    # Use all budget on attempt1.
    for _ in range(settings.ai_interaction_cap):
        with _mock_llm_response():
            resp = client.post(
                "/ai/chat",
                json={"attempt_id": attempt1.id, "message": "help me"},
            )
        assert resp.status_code == 200

    # attempt1 is now exhausted.
    resp = client.post(
        "/ai/chat",
        json={"attempt_id": attempt1.id, "message": "help me"},
    )
    assert resp.status_code == 429

    # attempt2 still has a fresh budget.
    with _mock_llm_response():
        resp = client.post(
            "/ai/chat",
            json={"attempt_id": attempt2.id, "message": "help me"},
        )
    assert resp.status_code == 200
    assert resp.json()["remaining_interactions"] == settings.ai_interaction_cap - 1