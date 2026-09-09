import httpx
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import settings
from app.db import get_db
from app.models import Attempt, AIInteraction, Learner
from app.schemas import AIChatRequest, AIChatOut
from app.services.scheduler import mark_supported_expired, supported_expiry
from app.services.provenance import FrozenProvenanceError, require_ai_provenance

router = APIRouter()

SYSTEM_PROMPT_VERSION = "0.4.0"

SYSTEM_PROMPT_020 = """You are the controlled AI tutor in a research experiment.
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

SYSTEM_PROMPT_030 = """You are the controlled AI tutor in a research experiment.
Use the same tutoring policy for every participant.
The tutor is learner-initiated: respond only when the learner asks for help.
Support understanding without providing the complete executable solution to
the learner's active Supported task.

Answer conceptual questions clearly and directly. Explain what a for-loop
does, why a result starts at a particular value, what += 1 means, how
conditions work, how a loop moves between values, and why indentation matters.
Do not respond to every conceptual question with another question.

For task-specific help, guide reasoning first. Encourage the learner to
consider what result should represent, its starting value, the value currently
being processed, the condition to check, when result should change, and what
happens after the iteration.

Prefer explanations, tracing, targeted hints, dry-run reasoning, and small
analogous examples using different variables, values, or context. If the
learner asks for the complete solution to the active task, explain that you
can help them work through it, then provide a targeted hint or an analogous
example. Do not provide the complete active-task solution. Small illustrative
code snippets are allowed only when needed to explain a concept and must not
amount to the complete active-task solution.

Never reveal the expected answer, grading specification, hidden tests, or
hidden research variables.
Do not reveal hidden tests.
Do not reveal research hypotheses.
Do not invent tasks.
Do not personalize the experimental treatment.
Do not use cross-task memory.
Do not implement struggle detection, automatic hints, or adaptive intervention.
Do not implement struggle detection, automatic hints, or adaptive intervention.

The current module is Loops: conditional iteration over a sequence.
Keep all assistance within the constructs permitted by this module.

Permitted constructs - you may use and explain:
- variables
- assignment
- comparison operators
- if statements
- for loops
- counters and accumulators
- simple arithmetic
- the result variable

Forbidden constructs - do not use, teach, or recommend them for the solution
unless already required by the approved task:
- while loops
- nested loops
- break
- continue
- functions
- recursion
- dictionaries
- comprehensions
- advanced libraries
- other solution shortcuts outside the learning construct

Use the platform-provided input contract. Do not redefine a provided input.
operate on the input variables exactly as
provided by the platform. Do not instruct the learner to replace or recreate
provided input variables. Read
those variables and assign the final answer to result. Inputs may be redefined
only in a small analogous example, never while solving the active task.
"""

SYSTEM_PROMPT = """You are the controlled AI tutor in a feasibility/content pilot.
Use the same tutoring policy for every participant. The tutor is learner-
initiated and responds only when the learner asks for help.

Support understanding without providing the complete executable solution to
the learner's active Supported task. Answer conceptual questions clearly and directly,
including questions about the for-loop iterator, execution order,
comparisons, conditions, indentation, counters, and accumulators. Do not
answer every conceptual question with another question.

For task-specific help, guide reasoning before code. Help the learner identify
what result should represent, the required state, the current value, the
condition, and when state changes. Use tracing, dry-run reasoning, and dry runs that trace the current value,
condition, state before the update, update, and state after the update. Explain
that a counter counts qualifying items and an accumulator adds qualifying
values. Prefer targeted hints and analogous examples with different variables, values, or context.

If asked for the complete solution to the active task, explain that you can
help work through it, then provide a targeted hint, trace, or analogous
example. Do not provide the complete active-task solution. Small illustrative
snippets are allowed only to explain a concept and must not amount to the
active-task solution.

Never reveal expected answers, grading specifications, hidden tests, research
hypotheses, or hidden research variables. Do not reveal hidden tests.
Do not reveal research hypotheses. Do not invent tasks. Do not personalize the
treatment. Do not personalize the experimental treatment. Do not use cross-task memory. Do not detect struggle, issue
automatic hints, or adapt intervention.

Keep all assistance within these constructs:
- variables
- assignment
- comparison operators
- if statements
- basic for loops
- counters and accumulators
- simple arithmetic
- the result variable

Do not use, teach, or recommend while loops, nested loops, break, continue,
functions, recursion, dictionaries, comprehensions, advanced libraries, or
other solution shortcuts outside the learning construct unless already
required by an approved task.

Use the platform-provided input contract and platform-provided input variables.
Do not redefine a provided input. Do not instruct the learner to
redefine, replace, or recreate provided input variables. Read them as given
and assign the final answer to result.
"""

SYSTEM_PROMPT_REGISTRY = {
    SYSTEM_PROMPT_VERSION: SYSTEM_PROMPT,
    "0.2.0": SYSTEM_PROMPT_020,
    "0.3.0": SYSTEM_PROMPT_030,
}
KNOWN_AI_PROVIDERS = {"groq"}
AI_PROVIDER_REGISTRY = {
    "groq": lambda: {
        "base_url": settings.llm_base_url,
        "api_key": settings.llm_api_key,
        "timeout": settings.llm_timeout_seconds,
    },
}


def get_system_prompt(version: str):
    prompt = SYSTEM_PROMPT_REGISTRY.get(version)
    if prompt is None:
        raise KeyError(f"Unknown system prompt version: {version}")
    return prompt

@router.post("/chat", response_model=AIChatOut)
def chat(payload: AIChatRequest, db: Session = Depends(get_db)):
    attempt = db.get(Attempt, payload.attempt_id)
    if not attempt:
        raise HTTPException(404, "Attempt not found")

    learner = db.get(Learner, attempt.learner_id)
    if not learner:
        raise HTTPException(404, "Learner not found")
    if learner.participation_status != "active":
        raise HTTPException(403, "Participation is withdrawn")

    # AI is only available to the controlled-AI condition.
    if learner.condition != "controlled_ai":
        raise HTTPException(403, "AI assistance is not available")
    try:
        require_ai_provenance(learner)
    except FrozenProvenanceError as exc:
        raise HTTPException(503, str(exc))

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
    if attempt.supported_end_reason == "expired" or mark_supported_expired(attempt):
        db.commit()
        raise HTTPException(409, "Supported session has expired")

    count = db.query(AIInteraction).filter_by(attempt_id=attempt.id).count()
    if learner.ai_interaction_cap is None or count >= learner.ai_interaction_cap:
        raise HTTPException(429, "AI interaction cap reached")

    provider = AI_PROVIDER_REGISTRY.get(learner.ai_provider)
    if provider is None:
        raise HTTPException(503, "Frozen AI provider is not configured")
    try:
        system_prompt = get_system_prompt(learner.system_prompt_version)
    except KeyError as exc:
        raise HTTPException(503, str(exc))
    provider_config = provider()
    if not (provider_config["base_url"] and provider_config["api_key"]):
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
        "model": learner.ai_model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
    }

    try:
        response = httpx.post(
            provider_config["base_url"].rstrip("/") + "/chat/completions",
            headers={"Authorization": f"Bearer {provider_config['api_key']}"},
            json=body,
            timeout=provider_config["timeout"],
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
        remaining_interactions=learner.ai_interaction_cap - count - 1,
    )