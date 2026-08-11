from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import Learner, Task, Attempt

ALLOWED = {
    "immediate_only": {"immediate"},
    "immediate_delayed": {"immediate", "delayed", "criterion"},
    "full": {"immediate", "delayed", "transfer", "criterion"},
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
