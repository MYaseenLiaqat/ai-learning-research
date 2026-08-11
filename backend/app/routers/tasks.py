from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Attempt
from app.schemas import TaskOut, SubmitRequest, SubmitOut
from app.services.grader import grade_python
from app.services.scheduler import due_attempts

router = APIRouter()

@router.get("/learner/{learner_id}", response_model=list[TaskOut])
def get_due_tasks(learner_id: int, db: Session = Depends(get_db)):
    attempts = due_attempts(db, learner_id)
    return [
        TaskOut(
            id=a.task.id,
            concept_id=a.task.concept_id,
            type=a.task.type,
            prompt_text=a.task.prompt_text,
            scheduled_for=a.scheduled_for,
        )
        for a in attempts
    ]

@router.post("/{task_id}/submit", response_model=SubmitOut)
def submit_task(task_id: int, learner_id: int, payload: SubmitRequest, db: Session = Depends(get_db)):
    attempt = (
        db.query(Attempt)
        .filter_by(task_id=task_id, learner_id=learner_id)
        .filter(Attempt.completed_at.is_(None))
        .first()
    )
    if not attempt:
        raise HTTPException(404, "Due attempt not found")

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
