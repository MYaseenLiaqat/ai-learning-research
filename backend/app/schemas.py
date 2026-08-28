from datetime import datetime
from pydantic import BaseModel, Field

class LearnerCreate(BaseModel):
    prior_ability_score: float | None = None

class LearnerOut(BaseModel):
    id: int
    prior_ability_score: float | None
    condition: str
    measurement_arm: str
    created_at: datetime
    study_protocol_version: str | None = None
    learning_module_version: str | None = None
    system_prompt_version: str | None = None
    ai_provider: str | None = None
    ai_model: str | None = None
    ai_interaction_cap: int | None = None
    supported_phase_minutes: int | None = None
    participation_status: str = "active"

class TaskOut(BaseModel):
    id: int
    attempt_id: int
    concept_id: int
    type: str
    prompt_text: str
    scheduled_for: datetime
    remaining_interactions: int
    started_at: datetime | None = None
    expires_at: datetime | None = None

class TaskStartOut(TaskOut):
    pass

class SubmitRequest(BaseModel):
    code: str = Field(min_length=1, max_length=20000)

class SubmitOut(BaseModel):
    attempt_id: int
    score: float
    passed: bool
    feedback: list[str]

class AIChatRequest(BaseModel):
    attempt_id: int
    message: str = Field(min_length=1, max_length=5000)

class AIChatOut(BaseModel):
    sequence_num: int
    response: str
    remaining_interactions: int

class SessionStartOut(BaseModel):
    module: dict
    module_version: str
    started_at: datetime | None
    expires_at: datetime | None
