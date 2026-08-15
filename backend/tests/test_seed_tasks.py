"""Tests for Loops seed task prompts and version."""

from scripts.seed import TASK_VERSION, seed
from app.models import Task


def test_seeded_tasks_use_version_020(db_session):
    seed(db_session)
    assert {t.version for t in db_session.query(Task).all()} == {"0.2.0"}


def test_loops_prompts_explicitly_forbid_redefining_provided_input(db_session):
    expected = {
        "supported": "temperatures",
        "immediate": "scores",
        "delayed": "prices",
        "transfer": "temperatures",
        "criterion": "transactions",
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
