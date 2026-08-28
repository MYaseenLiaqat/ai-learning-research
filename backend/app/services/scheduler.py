from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.config import settings
from app.models import Learner, Task, Attempt
from app.services.provenance import FrozenProvenanceError, require_common_provenance

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
            task_version=task.version,
            scheduled_for=scheduled,
        ))
    db.commit()


def supported_expiry(attempt: Attempt):
    try:
        require_common_provenance(attempt.learner)
    except FrozenProvenanceError:
        raise
    minutes = attempt.learner.supported_phase_minutes
    if minutes is None:
        raise FrozenProvenanceError(
            "Frozen learner provenance is missing supported_phase_minutes"
        )
    return attempt.started_at + timedelta(minutes=minutes)


def mark_supported_expired(attempt: Attempt, now=None):
    if (
        attempt.task.type == "supported"
        and attempt.started_at is not None
        and attempt.completed_at is None
        and attempt.supported_end_reason is None
        and (now or datetime.utcnow()) >= supported_expiry(attempt)
    ):
        attempt.supported_end_reason = "expired"
        return True
    return False

def due_attempts(db: Session, learner_id: int):
    attempts = (
        db.query(Attempt)
        .filter(
            Attempt.learner_id == learner_id,
            Attempt.scheduled_for <= datetime.utcnow(),
            Attempt.completed_at.is_(None),
        )
        .all()
    )
    changed = any(mark_supported_expired(attempt) for attempt in attempts)
    if changed:
        db.commit()
    return attempts

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
    if supported.supported_end_reason == "expired":
        return True
    if supported.started_at is not None:
        if mark_supported_expired(supported):
            db.commit()
            return True
    return False
