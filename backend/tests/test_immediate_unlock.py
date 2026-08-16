from datetime import datetime, timedelta


def _task_types(client, learner_id):
    resp = client.get(f"/tasks/learner/{learner_id}")
    assert resp.status_code == 200
    return {t["type"] for t in resp.json()}


def test_immediate_hidden_before_session_start(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    supported = make_task("supported")
    immediate = make_task("immediate")
    make_attempt(learner, supported)
    make_attempt(learner, immediate)

    types = _task_types(client, learner.id)

    assert "supported" in types
    assert "immediate" not in types


def test_supported_visible_before_session_start(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    supported = make_task("supported")
    make_attempt(learner, supported)

    types = _task_types(client, learner.id)

    assert "supported" in types


def test_immediate_hidden_during_active_incomplete_supported(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    supported = make_task("supported")
    immediate = make_task("immediate")
    make_attempt(learner, supported, started_at=datetime.utcnow())
    make_attempt(learner, immediate)

    types = _task_types(client, learner.id)

    assert "supported" in types
    assert "immediate" not in types


def test_supported_visible_during_active_incomplete_session(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    supported = make_task("supported")
    make_attempt(learner, supported, started_at=datetime.utcnow())

    types = _task_types(client, learner.id)

    assert "supported" in types


def test_immediate_available_after_supported_completion(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    supported = make_task("supported")
    immediate = make_task("immediate")
    make_attempt(learner, supported, started_at=datetime.utcnow(), completed_at=datetime.utcnow())
    make_attempt(learner, immediate)

    types = _task_types(client, learner.id)

    assert "immediate" in types
    assert "supported" not in types


def test_supported_hidden_after_expiry(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    supported = make_task("supported")
    # Supported started 21 minutes ago (> 20 min limit), not completed.
    make_attempt(
        learner,
        supported,
        started_at=datetime.utcnow() - timedelta(minutes=21),
    )

    types = _task_types(client, learner.id)

    assert "supported" not in types


def test_delayed_transfer_criterion_scheduling_unchanged(
    client, db_session, make_learner, make_task, make_attempt
):
    """Delayed/Transfer/Criterion remain hidden until their scheduled offset."""
    learner = make_learner()
    delayed = make_task("delayed", offset_days=7)
    transfer = make_task("transfer", offset_days=14)
    criterion = make_task("criterion", offset_days=21)
    make_attempt(learner, delayed, scheduled_for=datetime.utcnow() + timedelta(days=7))
    make_attempt(learner, transfer, scheduled_for=datetime.utcnow() + timedelta(days=14))
    make_attempt(learner, criterion, scheduled_for=datetime.utcnow() + timedelta(days=21))

    types = _task_types(client, learner.id)

    assert "delayed" not in types
    assert "transfer" not in types
    assert "criterion" not in types
    assert "supported" not in types


def test_supported_hidden_after_completion(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    supported = make_task("supported")
    make_attempt(learner, supported, started_at=datetime.utcnow(), completed_at=datetime.utcnow())

    types = _task_types(client, learner.id)

    assert "supported" not in types


def test_immediate_available_after_supported_expiry(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    supported = make_task("supported")
    immediate = make_task("immediate")
    # Supported started 21 minutes ago (> 20 min limit), not completed.
    make_attempt(
        learner,
        supported,
        started_at=datetime.utcnow() - timedelta(minutes=21),
    )
    make_attempt(learner, immediate)

    types = _task_types(client, learner.id)

    assert "immediate" in types