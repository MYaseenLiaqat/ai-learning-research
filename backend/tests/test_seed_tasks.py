"""Tests for Loops seed task prompts and version."""

from scripts.seed import TASK_VERSION, seed
from app.models import Task


def test_seeded_tasks_use_version_050(db_session):
    seed(db_session)
    assert {t.version for t in db_session.query(Task).all()} == {"0.5.0"}


def test_criterion_differs_from_delayed_and_remains_within_loop_construct(db_session):
    seed(db_session)
    tasks = {t.type: t for t in db_session.query(Task).all()}
    delayed_prompt = tasks["delayed"].prompt_text
    criterion_prompt = tasks["criterion"].prompt_text

    assert "activity" in criterion_prompt
    assert "strictly greater than 1000" not in criterion_prompt
    assert criterion_prompt.startswith(
        "The platform already provides a variable named `activity` containing:"
    )
    assert "longest consecutive" in criterion_prompt
    assert "current-streak state" in criterion_prompt
    assert "platform already provides a variable named" in criterion_prompt
    assert "Do not redefine" in criterion_prompt
    assert "result" in criterion_prompt
    assert "ages" in delayed_prompt
    assert "criterion" not in criterion_prompt.lower()


def test_criterion_hidden_expected_values_remain_unchanged(db_session):
    seed(db_session)
    criterion = db_session.query(Task).filter_by(type="criterion").one()
    assert [case["expected"] for case in criterion.grading_spec["tests"]] == [
        3, 0, 0, 1, 2, 2
    ]


def test_assessment_prompts_do_not_expose_expected_answers(db_session):
    seed(db_session)
    tasks = db_session.query(Task).all()
    for task in tasks:
        assert "Expected result:" not in task.prompt_text
        assert "Expected result" not in task.prompt_text
        assert "expected result" not in task.prompt_text.lower()


def test_loops_prompts_explicitly_forbid_redefining_provided_input(db_session):
    expected = {
        "supported": "temperatures",
        "immediate": "scores",
        "delayed": "ages",
        "transfer": "scores",
        "criterion": "activity",
    }
    seed(db_session)
    tasks = db_session.query(Task).all()
    types = {t.type: t for t in tasks}
    assert set(types) == set(expected)
    for task_type, var in expected.items():
        prompt = types[task_type].prompt_text
        assert "The platform already provides a variable named" in prompt
        tick = chr(96)
        assert "Do not redefine " + tick + var + tick in prompt
