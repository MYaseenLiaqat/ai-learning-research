def test_learning_module_retrieval(client, make_learner):
    learner = make_learner()
    resp = client.get(f"/learning/loops?learner_id={learner.id}")

    assert resp.status_code == 200
    data = resp.json()
    assert data["module_id"] == "loops"
    assert data["version"] == "v0.2.0"
    assert "explanation" in data
    assert "worked_example" in data
    assert "guided_practice" in data
    assert "static_hints" in data
    assert len(data["static_hints"]) == 3


def test_learning_material_identical_across_conditions(client, make_learner):
    # Both conditions call the same unauthenticated, condition-independent endpoint.
    ai = make_learner(condition="controlled_ai")
    no_ai = make_learner(condition="no_ai")
    ai_resp = client.get(f"/learning/loops?learner_id={ai.id}")
    no_ai_resp = client.get(f"/learning/loops?learner_id={no_ai.id}")

    assert ai_resp.status_code == 200
    assert no_ai_resp.status_code == 200
    # Identical material content for both conditions.
    assert ai_resp.json() == no_ai_resp.json()


def test_get_learning_loops_does_not_start_session(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner(condition="controlled_ai")
    task = make_task("supported")
    attempt = make_attempt(learner, task)

    resp = client.get(f"/learning/loops?learner_id={learner.id}")

    assert resp.status_code == 200
    db_session.refresh(attempt)
    assert attempt.started_at is None


def test_task_listing_does_not_start_session(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner(condition="controlled_ai")
    task = make_task("supported")
    attempt = make_attempt(learner, task)

    resp = client.get(f"/tasks/learner/{learner.id}")

    assert resp.status_code == 200
    db_session.refresh(attempt)
    assert attempt.started_at is None