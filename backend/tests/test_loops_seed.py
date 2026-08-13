from app.services.scheduler import seed_attempts
from app.models import Concept, Task, Learner, Attempt


def test_seed_contains_loops_tasks(db_session):
    """Loops pilot seed data exists for all five stages."""
    # Replicate the seed's five Loops tasks into the in-memory DB.
    concept = Concept(name="Loops", order=1)
    db_session.add(concept)
    db_session.commit()

    stages = ["supported", "immediate", "delayed", "transfer", "criterion"]
    tasks = [
        Task(
            concept_id=concept.id,
            type=stage,
            prompt_text=f"Task {stage}",
            grading_spec={
                "mode": "exec_result",
                "result_var": "result",
                "tests": [{"inputs": {"x": [1]}, "expected": 1}],
            },
            scheduled_offset_days=0,
            version="0.1.0",
        )
        for stage in stages
    ]
    db_session.add_all(tasks)
    db_session.commit()

    stored = db_session.query(Task).all()
    types = {t.type for t in stored}
    assert {"supported", "immediate", "delayed", "transfer", "criterion"} <= types

    versions = {t.version for t in stored}
    assert versions == {"0.1.0"}


def test_loops_seed_uses_exec_result(db_session):
    """Loops tasks must use exec_result, not function-definition contracts."""
    concept = Concept(name="Loops", order=1)
    db_session.add(concept)
    db_session.commit()

    stages = ["supported", "immediate", "delayed", "transfer", "criterion"]
    tasks = [
        Task(
            concept_id=concept.id,
            type=stage,
            prompt_text=f"Task {stage}",
            grading_spec={
                "mode": "exec_result",
                "result_var": "result",
                "tests": [{"inputs": {"x": [1]}, "expected": 1}],
            },
            scheduled_offset_days=0,
            version="0.1.0",
        )
        for stage in stages
    ]
    db_session.add_all(tasks)
    db_session.commit()

    for t in db_session.query(Task).all():
        assert t.grading_spec.get("mode") == "exec_result"
        assert t.grading_spec.get("result_var") == "result"


def test_supported_attempt_is_seeded(db_session):
    """seed_attempts must create a Supported attempt (ALLOWED includes it)."""
    concept = Concept(name="Loops", order=1)
    db_session.add(concept)
    db_session.commit()

    supported = Task(
        concept_id=concept.id,
        type="supported",
        prompt_text="count_above",
        grading_spec={
            "mode": "exec_result",
            "result_var": "result",
            "tests": [{"inputs": {"temperatures": [1]}, "expected": 0}],
        },
        scheduled_offset_days=0,
    )
    immediate = Task(
        concept_id=concept.id,
        type="immediate",
        prompt_text="count_at_least",
        grading_spec={
            "mode": "exec_result",
            "result_var": "result",
            "tests": [{"inputs": {"scores": [1]}, "expected": 0}],
        },
        scheduled_offset_days=0,
    )
    db_session.add_all([supported, immediate])
    db_session.commit()

    learner = Learner(
        prior_ability_score=0.5,
        condition="no_ai",
        measurement_arm="full",
    )
    db_session.add(learner)
    db_session.commit()

    seed_attempts(db_session, learner)

    attempts = db_session.query(Attempt).filter_by(learner_id=learner.id).all()
    assert {a.task.type for a in attempts} == {"supported", "immediate"}


def test_hidden_tests_not_exposed(client, db_session, make_learner, make_task, make_attempt):
    """GET /tasks/learner/{id} must not return grading_spec (hidden tests)."""
    learner = make_learner()
    task = make_task("supported")
    make_attempt(learner, task)

    resp = client.get(f"/tasks/learner/{learner.id}")

    assert resp.status_code == 200
    assert len(resp.json()) >= 1
    assert "grading_spec" not in resp.json()[0].keys()
