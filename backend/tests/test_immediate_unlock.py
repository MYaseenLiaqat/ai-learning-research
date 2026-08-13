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