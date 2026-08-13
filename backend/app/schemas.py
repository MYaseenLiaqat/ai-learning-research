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

class TaskOut(BaseModel):
    id: int
    concept_id: int
    type: str
    prompt_text: str
    scheduled_for: datetime

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
