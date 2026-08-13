import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import Learner, Concept, Task, Attempt


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def concept(db_session):
    c = Concept(name="Loops", order=1)
    db_session.add(c)
    db_session.commit()
    db_session.refresh(c)
    return c


@pytest.fixture()
def make_task(db_session, concept):
    def _make_task(task_type, offset_days=0):
        t = Task(
            concept_id=concept.id,
            type=task_type,
            prompt_text=f"Task {task_type}",
            grading_spec={"tests": [
                {"expression": "add(1,2)", "expected": 3},
            ]},
            scheduled_offset_days=offset_days,
        )
        db_session.add(t)
        db_session.commit()
        db_session.refresh(t)
        return t
    return _make_task


@pytest.fixture()
def make_learner(db_session):
    def _make_learner(condition="controlled_ai"):
        l = Learner(
            prior_ability_score=0.5,
            condition=condition,
            measurement_arm="full",
        )
        db_session.add(l)
        db_session.commit()
        db_session.refresh(l)
        return l
    return _make_learner


@pytest.fixture()
def make_attempt(db_session):
    def _make_attempt(learner, task, scheduled_for=None, completed_at=None):
        a = Attempt(
            learner_id=learner.id,
            task_id=task.id,
            scheduled_for=scheduled_for or datetime.utcnow(),
            completed_at=completed_at,
        )
        db_session.add(a)
        db_session.commit()
        db_session.refresh(a)
        return a
    return _make_attempt