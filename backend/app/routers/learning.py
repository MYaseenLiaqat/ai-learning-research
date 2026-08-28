from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import settings
from app.db import get_db
from app.models import Attempt, Learner, Task
from app.schemas import SessionStartOut
from app.services.learning_material import get_learning_module
from app.services.scheduler import mark_supported_expired, supported_expiry
from app.services.provenance import FrozenProvenanceError, require_common_provenance

router = APIRouter()


@router.get("/loops")
def get_loops_module(learner_id: int, db: Session = Depends(get_db)):
    """Return the static Loops learning material.

    Does NOT start the Supported-session timer.
    """
    learner = db.get(Learner, learner_id)
    if not learner:
        raise HTTPException(404, "Learner not found")
    try:
        require_common_provenance(learner)
    except FrozenProvenanceError as exc:
        raise HTTPException(503, str(exc))
    if learner.participation_status != "active":
        raise HTTPException(403, "Participation is withdrawn")
    try:
        return get_learning_module(learner.learning_module_version)
    except KeyError as exc:
        raise HTTPException(503, str(exc))


@router.post("/loops/start", response_model=SessionStartOut)
def start_loops_session(learner_id: int, db: Session = Depends(get_db)):
    """Explicitly start the Supported-session timer.

    This is the ONLY event that starts the 20-minute Supported-session clock.
    A second call returns the existing timestamps without resetting the timer.
    """
    learner = db.get(Learner, learner_id)
    if not learner:
        raise HTTPException(404, "Learner not found")
    try:
        require_common_provenance(learner)
    except FrozenProvenanceError as exc:
        raise HTTPException(503, str(exc))
    if learner.participation_status != "active":
        raise HTTPException(403, "Participation is withdrawn")

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

    if mark_supported_expired(supported):
        db.commit()
    if supported.supported_end_reason == "expired":
        raise HTTPException(409, "Supported session has expired")
    if supported.completed_at is not None or supported.supported_end_reason == "completed":
        raise HTTPException(409, "Supported session has already completed")

    if supported.started_at is None:
        supported.started_at = datetime.utcnow()
        supported.module_version = learner.learning_module_version
        db.commit()

    started_at = supported.started_at
    expires_at = supported_expiry(supported)
    try:
        module = get_learning_module(learner.learning_module_version)
    except KeyError as exc:
        raise HTTPException(503, str(exc))

    return SessionStartOut(
        module=module,
        module_version=learner.learning_module_version,
        started_at=started_at,
        expires_at=expires_at,
    )