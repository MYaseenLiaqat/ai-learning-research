from datetime import datetime, timedelta


def test_valid_due_attempt_can_be_submitted_and_graded(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    task = make_task("immediate")
    attempt = make_attempt(learner, task)

    resp = client.post(
        f"/tasks/{task.id}/submit",
        params={"learner_id": learner.id},
        json={"code": "def add(a,b):\n    return a+b\n"},
    )

    assert resp.status_code == 200
    data = resp.json()
    assert data["attempt_id"] == attempt.id
    assert data["score"] == 1.0
    assert data["passed"] is True

    db_session.refresh(attempt)
    assert attempt.completed_at is not None
    assert attempt.score == 1.0


def test_future_task_submission_is_rejected(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    task = make_task("delayed")
    attempt = make_attempt(
        learner, task, scheduled_for=datetime.utcnow() + timedelta(days=7)
    )

    resp = client.post(
        f"/tasks/{task.id}/submit",
        params={"learner_id": learner.id},
        json={"code": "def add(a,b):\n    return a+b\n"},
    )

    assert resp.status_code == 409

    db_session.refresh(attempt)
    assert attempt.completed_at is None


def test_unassigned_learner_task_submission_is_rejected(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    task = make_task("immediate")
    make_attempt(learner, task)

    other_learner = make_learner()

    resp = client.post(
        f"/tasks/{task.id}/submit",
        params={"learner_id": other_learner.id},
        json={"code": "def add(a,b):\n    return a+b\n"},
    )

    assert resp.status_code == 404


def test_completed_attempt_cannot_be_resubmitted(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    task = make_task("immediate")
    attempt = make_attempt(learner, task, completed_at=datetime.utcnow())

    resp = client.post(
        f"/tasks/{task.id}/submit",
        params={"learner_id": learner.id},
        json={"code": "def add(a,b):\n    return a+b\n"},
    )

    assert resp.status_code == 409


def test_nonexistent_learner_submission_is_rejected(
    client, db_session, make_task, make_attempt
):
    task = make_task("immediate")

    resp = client.post(
        f"/tasks/{task.id}/submit",
        params={"learner_id": 9999},
        json={"code": "def add(a,b):\n    return a+b\n"},
    )

    assert resp.status_code == 404