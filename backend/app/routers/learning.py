from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import settings
from app.db import get_db
from app.models import Attempt, Learner, Task
from app.schemas import SessionStartOut
from app.services.learning_material import LOOPS_MODULE

router = APIRouter()


@router.get("/loops")
def get_loops_module():
    """Return the static Loops learning material.

    Does NOT start the Supported-session timer.
    """
    return LOOPS_MODULE


@router.post("/loops/start", response_model=SessionStartOut)
def start_loops_session(learner_id: int, db: Session = Depends(get_db)):
    """Explicitly start the Supported-session timer.

    This is the ONLY event that starts the 20-minute Supported-session clock.
    A second call returns the existing timestamps without resetting the timer.
    """
    learner = db.get(Learner, learner_id)
    if not learner:
        raise HTTPException(404, "Learner not found")

    supported = (
        db.query(Attempt)
        .join(Task)
        .filter(
            Attempt.learner_id == learner_id,
            Task.type == "supported",
        )
        .first()
    )
    if not supported:
        raise HTTPException(404, "Supported attempt not found")

    if supported.started_at is None:
        supported.started_at = datetime.utcnow()
        supported.module_version = LOOPS_MODULE["version"]
        db.commit()

    started_at = supported.started_at
    expires_at = started_at + timedelta(minutes=settings.supported_phase_minutes)

    return SessionStartOut(
        module=LOOPS_MODULE,
        module_version=LOOPS_MODULE["version"],
        started_at=started_at,
        expires_at=expires_at,
    )