from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import settings
from app.db import get_db
from app.models import Attempt, AIInteraction, Learner
from app.schemas import TaskOut, SubmitRequest, SubmitOut
from app.services.grader import grade_python
from app.services.scheduler import due_attempts, is_supported_completed_or_expired

router = APIRouter()


@router.get("/learner/{learner_id}", response_model=list[TaskOut])
def get_due_tasks(learner_id: int, db: Session = Depends(get_db)):
    """Return available tasks.

    Viewing tasks does NOT start the Supported-session timer.
    Immediate is only returned once the Supported phase is completed or expired.
    """
    attempts = due_attempts(db, learner_id)
    immediate_available = is_supported_completed_or_expired(db, learner_id)

    result = []
    for a in attempts:
        if a.task.type == "immediate" and not immediate_available:
            continue
        if a.task.type == "supported" and immediate_available:
            continue
        result.append(a)

    return [
        TaskOut(
            id=a.task.id,
            attempt_id=a.id,
            concept_id=a.task.concept_id,
            type=a.task.type,
            prompt_text=a.task.prompt_text,
            scheduled_for=a.scheduled_for,
            remaining_interactions=settings.ai_interaction_cap
            - db.query(AIInteraction).filter_by(attempt_id=a.id).count(),
            started_at=a.started_at,
            expires_at=(
                a.started_at + timedelta(minutes=settings.supported_phase_minutes)
                if a.started_at is not None
                else None
            ),
        )
        for a in result
    ]


@router.post("/{task_id}/submit", response_model=SubmitOut)
def submit_task(task_id: int, learner_id: int, payload: SubmitRequest, db: Session = Depends(get_db)):
    learner = db.get(Learner, learner_id)
    if not learner:
        raise HTTPException(404, "Learner not found")

    attempt = (
        db.query(Attempt)
        .filter_by(task_id=task_id, learner_id=learner_id)
        .first()
    )
    if not attempt:
        raise HTTPException(404, "Attempt not found")

    if attempt.completed_at is not None:
        raise HTTPException(409, "Attempt has already been completed")

    if attempt.scheduled_for > datetime.utcnow():
        raise HTTPException(409, "Attempt is not yet available")

    if attempt.task.type == "supported":
        # Supported submission requires an explicitly started session.
        if attempt.started_at is None:
            raise HTTPException(409, "Supported session has not started")
        expiry = attempt.started_at + timedelta(minutes=settings.supported_phase_minutes)
        if datetime.utcnow() > expiry:
            raise HTTPException(409, "Supported session has expired")
    elif attempt.task.type == "immediate":
        # Immediate is only available after Supported completes or expires.
        if not is_supported_completed_or_expired(db, learner_id):
            raise HTTPException(409, "Immediate assessment is not yet available")

    score, feedback = grade_python(payload.code, attempt.task.grading_spec)
    attempt.submitted_code = payload.code
    attempt.score = score
    attempt.graded_at = datetime.utcnow()
    attempt.completed_at = datetime.utcnow()
    db.commit()

    return SubmitOut(
        attempt_id=attempt.id,
        score=score,
        passed=score >= 1.0,
        feedback=feedback,
    )