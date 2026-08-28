from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import settings

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from app import models
    Base.metadata.create_all(bind=engine)
    _apply_lightweight_migrations()


def _apply_lightweight_migrations():
    """Idempotent ALTER TABLE guards for pilot schema additions.

    `create_all` does not alter existing tables. These guards add columns
    to SQLite databases created before the columns existed. They are no-ops
    if the column already exists or if using a non-SQLite backend.
    """
    if not settings.database_url.startswith("sqlite"):
        return
    inspector = inspect(engine)
    with engine.begin() as conn:
        learner_cols = {c["name"] for c in inspector.get_columns("learners")}
        learner_additions = {
            "study_protocol_version": "VARCHAR(30)",
            "learning_module_version": "VARCHAR(30)",
            "system_prompt_version": "VARCHAR(30)",
            "ai_provider": "VARCHAR(50)",
            "ai_model": "VARCHAR(100)",
            "ai_interaction_cap": "INTEGER",
            "supported_phase_minutes": "INTEGER",
            "participation_status": "VARCHAR(20)",
        }
        for name, definition in learner_additions.items():
            if name not in learner_cols:
                conn.exec_driver_sql(
                    f"ALTER TABLE learners ADD COLUMN {name} {definition}"
                )
        task_cols = {c["name"] for c in inspector.get_columns("tasks")}
        if "version" not in task_cols:
            conn.exec_driver_sql("ALTER TABLE tasks ADD COLUMN version VARCHAR(30)")
        attempt_cols = {c["name"] for c in inspector.get_columns("attempts")}
        if "started_at" not in attempt_cols:
            conn.exec_driver_sql("ALTER TABLE attempts ADD COLUMN started_at DATETIME")
        if "module_version" not in attempt_cols:
            conn.exec_driver_sql("ALTER TABLE attempts ADD COLUMN module_version VARCHAR(30)")
        if "task_version" not in attempt_cols:
            conn.exec_driver_sql("ALTER TABLE attempts ADD COLUMN task_version VARCHAR(30)")
        if "grader_version" not in attempt_cols:
            conn.exec_driver_sql("ALTER TABLE attempts ADD COLUMN grader_version VARCHAR(30)")
        if "supported_end_reason" not in attempt_cols:
            conn.exec_driver_sql("ALTER TABLE attempts ADD COLUMN supported_end_reason VARCHAR(20)")
