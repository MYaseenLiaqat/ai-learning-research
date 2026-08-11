import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Learner
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

@router.get("/{learner_id}", response_model=LearnerOut)
def get_learner(learner_id: int, db: Session = Depends(get_db)):
    learner = db.get(Learner, learner_id)
    if not learner:
        raise HTTPException(404, "Learner not found")
    return learner
