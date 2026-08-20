"""Regression tests: task-availability response must expose attempt_id."""

from datetime import datetime, timedelta

from app.models import Attempt


def _tasks(client, learner_id):
    resp = client.get(f"/tasks/learner/{learner_id}")
    assert resp.status_code == 200
    return resp.json()


def test_supported_task_includes_correct_attempt_id(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    task = make_task("supported")
    attempt = make_attempt(learner, task)

    tasks = _tasks(client, learner.id)
    supported = [t for t in tasks if t["type"] == "supported"]
    assert len(supported) == 1
    assert supported[0]["attempt_id"] == attempt.id
    assert supported[0]["id"] == task.id


def test_immediate_task_includes_correct_attempt_id_after_unlock(
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
    immediate_attempt = make_attempt(learner, immediate)

    tasks = _tasks(client, learner.id)
    immediate_tasks = [t for t in tasks if t["type"] == "immediate"]
    assert len(immediate_tasks) == 1
    assert immediate_tasks[0]["attempt_id"] == immediate_attempt.id
    assert immediate_tasks[0]["id"] == immediate.id


def test_attempt_id_belongs_to_correct_learner_and_task(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    task = make_task("supported")
    attempt = make_attempt(learner, task)

    tasks = _tasks(client, learner.id)
    supported = [t for t in tasks if t["type"] == "supported"][0]

    # The returned attempt_id must resolve to the same learner and task.
    stored = db_session.get(Attempt, supported["attempt_id"])
    assert stored is not None
    assert stored.learner_id == learner.id
    assert stored.task_id == task.id


def test_repeated_get_does_not_create_duplicate_attempts(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    task = make_task("supported")
    make_attempt(learner, task)

    before = db_session.query(Attempt).filter_by(learner_id=learner.id).count()

    for _ in range(3):
        _tasks(client, learner.id)

    after = db_session.query(Attempt).filter_by(learner_id=learner.id).count()
    assert after == before