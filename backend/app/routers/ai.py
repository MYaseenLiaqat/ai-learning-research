import httpx
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import settings
from app.db import get_db
from app.models import Attempt, AIInteraction, Learner
from app.schemas import AIChatRequest, AIChatOut

router = APIRouter()

SYSTEM_PROMPT_VERSION = "0.2.0"

SYSTEM_PROMPT = """You are the controlled AI tutor in a research experiment.
Use the same tutoring policy for every participant.
Give concise conceptual guidance and small hints.
Do not reveal hidden tests.
Do not reveal research hypotheses.
Do not invent tasks.
Do not personalize the experimental treatment.
Do not use cross-task memory.

The current module is Loops: conditional iteration over a sequence.

Keep all assistance within the constructs permitted by this module.

Permitted constructs - you may use and explain:
- variables
- assignment
- comparison operators
- if statements
- for loops
- counters and accumulators
- the result variable

Forbidden constructs - do not use, teach, or recommend them for the solution:
- list comprehensions
- while loops
- nested loops
- break
- continue
- functions as the solution abstraction
- recursion
- dictionaries
- advanced libraries
- any other shortcut that bypasses the for-loop construct

If the learner requests a complete solution, you may provide one, but it must
use only the permitted constructs above.

For the actual task solution, operate on the input variables exactly as
provided by the platform. Do not redefine a provided input in the solution.
For example, do not reassign the input list; you may create new variables
such as a counter or accumulator, and assign the final answer to the result
variable.

You may redefine a provided input only in a small illustrative example,
never while solving the actual task.
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

    # The Supported session must have been explicitly started.
    if attempt.started_at is None:
        raise HTTPException(409, "Supported session has not started")

    # Enforce Supported-session time limit.
    expiry = attempt.started_at + timedelta(minutes=settings.supported_phase_minutes)
    if datetime.utcnow() > expiry:
        raise HTTPException(409, "Supported session has expired")

    count = db.query(AIInteraction).filter_by(attempt_id=attempt.id).count()
    if count >= settings.ai_interaction_cap:
        raise HTTPException(429, "AI interaction cap reached")

    if not (settings.llm_base_url and settings.llm_api_key and settings.llm_model):
        raise HTTPException(status_code=503, detail="AI provider is not configured")

    spec = attempt.task.grading_spec or {}
    input_names = []
    if spec.get("mode") == "exec_result":
        for test in spec.get("tests", []):
            for key in test.get("inputs", {}):
                if key not in input_names:
                    input_names.append(key)
    input_names.sort()

    context_bits = [f"Task:\n{attempt.task.prompt_text}\n\nLearner:\n{payload.message}"]
    if input_names:
        context_bits.append(
            "Platform-provided input variables: "
            + ", ".join(input_names)
            + '.\nThese variables are already defined by the platform. Never assign to, redefine, replace, or recreate them in the solution. Only read from them and assign the final answer to `result`.'
        )
    user_content = "\n\n".join(context_bits)

    body = {
        "model": settings.llm_model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
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