import random
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Attempt, Learner
from app.schemas import LearnerCreate, LearnerOut
from app.services.scheduler import seed_attempts

router = APIRouter()

@router.post("", response_model=LearnerOut)
def create_learner(payload: LearnerCreate, db: Session = Depends(get_db)):
    learner = Learner(
        prior_ability_score=payload.prior_ability_score,
        condition=random.choice(["no_ai", "controlled_ai"]),
        measurement_arm=random.choice(["immediate_only", "immediate_delayed", "full"]),
    )
    db.add(learner)
    db.commit()
    db.refresh(learner)
    seed_attempts(db, learner)
    return learner

class LearnerStatusOut(BaseModel):
    learner_id: int
    has_future_assessments: bool
    next_assessment_at: datetime | None


@router.get("/{learner_id}", response_model=LearnerOut)
def get_learner(learner_id: int, db: Session = Depends(get_db)):
    learner = db.get(Learner, learner_id)
    if not learner:
        raise HTTPException(404, "Learner not found")
    return learner


@router.get("/{learner_id}/status", response_model=LearnerStatusOut)
def get_learner_status(learner_id: int, db: Session = Depends(get_db)):
    """Return whether the learner has future scheduled assessments.

    Used by the frontend to distinguish "return later" (future assessment
    exists) from "study complete" (nothing left). Does not unlock anything.
    """
    learner = db.get(Learner, learner_id)
    if not learner:
        raise HTTPException(404, "Learner not found")

    future = (
        db.query(Attempt)
        .filter(
            Attempt.learner_id == learner_id,
            Attempt.scheduled_for > datetime.utcnow(),
            Attempt.completed_at.is_(None),
        )
        .order_by(Attempt.scheduled_for.asc())
        .first()
    )

    return LearnerStatusOut(
        learner_id=learner.id,
        has_future_assessments=future is not None,
        next_assessment_at=future.scheduled_for if future else None,
    )
