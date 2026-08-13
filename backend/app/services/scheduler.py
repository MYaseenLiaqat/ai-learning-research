from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.config import settings
from app.models import Learner, Task, Attempt

ALLOWED = {
    "immediate_only": {"supported", "immediate"},
    "immediate_delayed": {"supported", "immediate", "delayed", "criterion"},
    "full": {"supported", "immediate", "delayed", "transfer", "criterion"},
}

def seed_attempts(db: Session, learner: Learner):
    existing = {
        a.task_id for a in db.query(Attempt).filter_by(learner_id=learner.id).all()
    }
    for task in db.query(Task).filter_by(active=True).all():
        if task.id in existing or task.type not in ALLOWED[learner.measurement_arm]:
            continue
        scheduled = learner.created_at + timedelta(days=task.scheduled_offset_days)
        db.add(Attempt(
            learner_id=learner.id,
            task_id=task.id,
            scheduled_for=scheduled,
        ))
    db.commit()

def due_attempts(db: Session, learner_id: int):
    return (
        db.query(Attempt)
        .filter(
            Attempt.learner_id == learner_id,
            Attempt.scheduled_for <= datetime.utcnow(),
            Attempt.completed_at.is_(None),
        )
        .all()
    )

def is_supported_completed_or_expired(db: Session, learner_id: int) -> bool:
    """Whether the Immediate assessment is unlocked.

    Immediate unlocks when the Supported attempt is completed OR its
    20-minute window has expired. It is NOT unlocked merely because its
    scheduled offset is zero.
    """
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
        return False
    if supported.completed_at is not None:
        return True
    if supported.started_at is not None:
        expiry = supported.started_at + timedelta(minutes=settings.supported_phase_minutes)
        if datetime.utcnow() > expiry:
            return True
    return False
