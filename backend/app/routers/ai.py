import httpx
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import settings
from app.db import get_db
from app.models import Attempt, AIInteraction, Learner
from app.schemas import AIChatRequest, AIChatOut

router = APIRouter()

SYSTEM_PROMPT = """You are the controlled AI tutor in a research experiment.
Use the same tutoring policy for every participant.
Give concise conceptual guidance and small hints.
Do not reveal hidden tests.
Do not invent tasks.
Do not personalize the experimental treatment.
"""

@router.post("/chat", response_model=AIChatOut)
def chat(payload: AIChatRequest, db: Session = Depends(get_db)):
    attempt = db.get(Attempt, payload.attempt_id)
    if not attempt:
        raise HTTPException(404, "Attempt not found")

    learner = db.get(Learner, attempt.learner_id)
    if not learner:
        raise HTTPException(404, "Learner not found")

    # AI is only available to the controlled-AI condition.
    if learner.condition != "controlled_ai":
        raise HTTPException(403, "AI assistance is not available")

    # AI is only available during the Supported learning phase.
    if attempt.task.type != "supported":
        raise HTTPException(403, "AI assistance is not available during this phase")

    # The attempt must be currently available.
    if attempt.scheduled_for > datetime.utcnow():
        raise HTTPException(409, "Attempt is not yet available")

    # The attempt must not already be completed.
    if attempt.completed_at is not None:
        raise HTTPException(409, "Attempt has already been completed")

    count = db.query(AIInteraction).filter_by(attempt_id=attempt.id).count()
    if count >= settings.ai_interaction_cap:
        raise HTTPException(429, "AI interaction cap reached")

    if not (settings.llm_base_url and settings.llm_api_key and settings.llm_model):
        raise HTTPException(503, "AI provider is not configured")

    body = {
        "model": settings.llm_model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Task:\n{attempt.task.prompt_text}\n\nLearner:\n{payload.message}",
            },
        ],
    }

    try:
        response = httpx.post(
            settings.llm_base_url.rstrip("/") + "/chat/completions",
            headers={"Authorization": f"Bearer {settings.llm_api_key}"},
            json=body,
            timeout=settings.llm_timeout_seconds,
        )
        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"]
    except Exception as exc:
        raise HTTPException(502, f"AI provider error: {exc}")

    interaction = AIInteraction(
        attempt_id=attempt.id,
        prompt=payload.message,
        response=answer,
        sequence_num=count + 1,
    )
    db.add(interaction)
    db.commit()

    return AIChatOut(
        sequence_num=count + 1,
        response=answer,
        remaining_interactions=settings.ai_interaction_cap - count - 1,
    )