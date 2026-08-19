import pytest
from datetime import datetime, timedelta
from unittest.mock import patch

from app.config import settings
from app.models import AIInteraction, Attempt


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


def test_supported_started_at_persists_and_refetch_does_not_restart(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    task = make_task("supported")
    make_attempt(learner, task)

    first = client.post(f"/learning/loops/start?learner_id={learner.id}")
    assert first.status_code == 200
    first_started = first.json()["started_at"]
    first_expires = first.json()["expires_at"]

    # Refetching the task list must not alter the timer.
    refetch = client.get(f"/tasks/learner/{learner.id}")
    assert refetch.status_code == 200

    # Explicit repeat start returns identical, non-reset timestamps.
    second = client.post(f"/learning/loops/start?learner_id={learner.id}")
    assert second.status_code == 200
    assert second.json()["started_at"] == first_started
    assert second.json()["expires_at"] == first_expires


def test_supported_expiry_computed_server_side_from_persisted_started_at(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    task = make_task("supported")
    # Persisted started_at 21 minutes ago (> 20-minute pilot window).
    make_attempt(
        learner,
        task,
        started_at=datetime.utcnow() - timedelta(minutes=21),
    )

    resp = client.post(
        f"/tasks/{task.id}/submit",
        params={"learner_id": learner.id},
        json={"code": "def add(a,b):\n    return a+b\n"},
    )

    assert resp.status_code == 409


def test_completed_supported_attempt_cannot_be_submitted_again(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    task = make_task("supported")
    make_attempt(
        learner,
        task,
        started_at=datetime.utcnow(),
        completed_at=datetime.utcnow(),
    )

    resp = client.post(
        f"/tasks/{task.id}/submit",
        params={"learner_id": learner.id},
        json={"code": "def add(a,b):\n    return a+b\n"},
    )

    assert resp.status_code == 409


def test_expired_supported_attempt_cannot_create_new_supported_session(
    client, db_session, make_learner, make_task, make_attempt
):
    """An expired Supported attempt must not unlock a second Supported window."""
    learner = make_learner()
    task = make_task("supported")
    # Expired (21 minutes ago), not completed.
    make_attempt(
        learner,
        task,
        started_at=datetime.utcnow() - timedelta(minutes=21),
    )

    # Attempting to start the session again must not reset or grant a new one.
    start_resp = client.post(f"/learning/loops/start?learner_id={learner.id}")
    assert start_resp.status_code == 200
    started = start_resp.json()["started_at"]
    # started_at is the persisted (now-expired) original start, not a reset.
    assert datetime.fromisoformat(started) < datetime.utcnow() - timedelta(minutes=20)

    # Submission must still be rejected as expired.
    sub = client.post(
        f"/tasks/{task.id}/submit",
        params={"learner_id": learner.id},
        json={"code": "result = 0\n"},
    )
    assert sub.status_code == 409


def test_immediate_submit_rejected_directly_before_supported_completion(
    client, db_session, make_learner, make_task, make_attempt
):
    """Direct endpoint access to Immediate is blocked before Supported finishes."""
    learner = make_learner()
    supported = make_task("supported")
    immediate = make_task("immediate")
    make_attempt(learner, supported, started_at=datetime.utcnow())
    make_attempt(learner, immediate)

    resp = client.post(
        f"/tasks/{immediate.id}/submit",
        params={"learner_id": learner.id},
        json={"code": "def add(a,b):\n    return a+b\n"},
    )

    assert resp.status_code == 409


def test_immediate_submit_allowed_directly_after_supported_completion(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    supported = make_task("supported")
    immediate = make_task("immediate")
    make_attempt(
        learner,
        supported,
        started_at=datetime.utcnow(),
        completed_at=datetime.utcnow(),
    )
    make_attempt(learner, immediate)

    resp = client.post(
        f"/tasks/{immediate.id}/submit",
        params={"learner_id": learner.id},
        json={"code": "def add(a,b):\n    return a+b\n"},
    )

    assert resp.status_code == 200


def test_immediate_submit_allowed_directly_after_supported_expiry(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    supported = make_task("supported")
    immediate = make_task("immediate")
    make_attempt(
        learner,
        supported,
        started_at=datetime.utcnow() - timedelta(minutes=21),
    )
    make_attempt(learner, immediate)

    resp = client.post(
        f"/tasks/{immediate.id}/submit",
        params={"learner_id": learner.id},
        json={"code": "def add(a,b):\n    return a+b\n"},
    )

    assert resp.status_code == 200


def test_transfer_and_criterion_rejected_before_scheduled_for(
    client, db_session, make_learner, make_task, make_attempt
):
    """Transfer/Criterion cannot be accessed before their scheduled_for date."""
    learner = make_learner()
    delayed = make_task("delayed")
    transfer = make_task("transfer")
    criterion = make_task("criterion")
    make_attempt(
        learner,
        delayed,
        scheduled_for=datetime.utcnow() + timedelta(days=7),
    )
    make_attempt(
        learner,
        transfer,
        scheduled_for=datetime.utcnow() + timedelta(days=14),
    )
    make_attempt(
        learner,
        criterion,
        scheduled_for=datetime.utcnow() + timedelta(days=21),
    )

    for t in (delayed, transfer, criterion):
        resp = client.post(
            f"/tasks/{t.id}/submit",
            params={"learner_id": learner.id},
            json={"code": "def add(a,b):\n    return a+b\n"},
        )
        assert resp.status_code == 409


def test_ai_cap_not_exceeded_across_reconnects(
    client, db_session, make_learner, make_task, make_attempt, monkeypatch
):
    """AI usage cannot exceed the configured cap, even across reconnect/refresh."""
    _configure_llm(monkeypatch)
    learner = make_learner(condition="controlled_ai")
    task = make_task("supported")
    attempt = make_attempt(learner, task, started_at=datetime.utcnow())

    cap = settings.ai_interaction_cap
    for i in range(cap):
        with _mock_llm_response():
            resp = client.post(
                "/ai/chat",
                json={"attempt_id": attempt.id, "message": f"msg {i}"},
            )
        assert resp.status_code == 200
        assert resp.json()["remaining_interactions"] == cap - i - 1

    # Exceeding the cap must be rejected (429), even "after reconnect".
    resp = client.post(
        "/ai/chat",
        json={"attempt_id": attempt.id, "message": "over the cap"},
    )
    assert resp.status_code == 429

    # Persisted interaction count must equal the cap, never more.
    count = db_session.query(AIInteraction).filter_by(attempt_id=attempt.id).count()
    assert count == cap


def test_ai_interactions_tied_to_correct_learner_and_attempt(
    client, db_session, make_learner, make_task, make_attempt, monkeypatch
):
    _configure_llm(monkeypatch)
    learner = make_learner(condition="controlled_ai")
    task = make_task("supported")
    attempt1 = make_attempt(learner, task, started_at=datetime.utcnow())

    with _mock_llm_response():
        resp = client.post(
            "/ai/chat",
            json={"attempt_id": attempt1.id, "message": "for attempt 1"},
        )
    assert resp.status_code == 200

    # A second Supported attempt for the same learner gets its own budget.
    task2 = make_task("supported")
    attempt2 = make_attempt(learner, task2, started_at=datetime.utcnow())
    with _mock_llm_response():
        resp = client.post(
            "/ai/chat",
            json={"attempt_id": attempt2.id, "message": "for attempt 2"},
        )
    assert resp.status_code == 200

    rows1 = db_session.query(AIInteraction).filter_by(attempt_id=attempt1.id).all()
    rows2 = db_session.query(AIInteraction).filter_by(attempt_id=attempt2.id).all()
    assert len(rows1) == 1
    assert len(rows2) == 1
    assert rows1[0].prompt == "for attempt 1"
    assert rows2[0].prompt == "for attempt 2"
    # Attempts belong to the same learner, but interactions are attempt-scoped.
    assert rows1[0].attempt_id == attempt1.id
    assert rows2[0].attempt_id == attempt2.id
