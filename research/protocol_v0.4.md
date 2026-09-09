# AI-Assisted Learning Study — Protocol v0.4

## Status
Current content-pilot protocol. Historical artifacts remain unchanged.

## Research question
Does pedagogically constrained AI tutoring during Supported programming practice change the relationship between immediate independent programming performance and subsequent unaided delayed retention and transfer?

Primary focus:
`Later outcome ~ Immediate + Condition + Immediate × Condition`

## Domain and construct
Current pilot domain: Python.
Current construct: basic conditional iteration with a `for` loop.

Target pattern:
`INITIALIZE → ITERATE → CHECK → UPDATE → RESULT`

Prerequisites:
variables, assignment, simple lists, comparisons, `if`, indentation, basic arithmetic, basic Python syntax.

Not target constructs:
`while`, nested loops, `break`, `continue`, functions, recursion, dictionaries, comprehensions, advanced libraries, or filtered-list construction as a required skill.

## Participants
Early-stage programmers with basic Python prerequisites; not complete novices or highly proficient/professional Python programmers.

Use `loops_prerequisite_screener_v0.3.md` to characterize readiness without directly pretesting Loops.

## Conditions
### No-AI
Standardized learning module + Supported task without generative AI.

### Controlled-AI
Identical instruction and Supported task plus learner-initiated pedagogical AI tutoring during Supported only.

All other instruction, timing, environment, grading, and assessments remain identical.

## AI treatment
System prompt: 0.3.0.
Working pilot controls: 20 minutes, maximum 8 successful interactions.

AI may explain concepts, trace execution, give targeted hints, use dry-run reasoning, and show small analogous examples.

AI must not provide the complete executable active-task solution, reveal hidden grader information, reveal research hypotheses, personalize treatment, or use cross-task memory.

No automatic struggle detection or adaptive intervention.

## Learning module
Current runtime version: v0.4.0.

It teaches:
1. how a `for` loop executes one value at a time;
2. conditions inside loops;
3. counting and summation.

Same module for both conditions.

## Task instrument
Current version: 0.4.0.

Stages:
- Supported: conditional counting
- Immediate: changed-context/boundary conditional counting
- Delayed: conditional summation
- Transfer: transformed conditional accumulation
- Criterion: less-scaffolded conditional summation in a new context

Participant prompts do not show expected results or hidden grader cases.

## Timing
Day 0: Learning → Supported → Immediate.
Delayed: target +7 days, working window ±2.
Transfer: target +14 days, working window ±2.
Criterion: target +21 days, working window ±3.

AI is unavailable server-side in all independent assessments.

## Reminders
Use standardized manual reminders containing scheduling information only. No hints, syntax, examples, or target-construct cues.

## Grading
Grader version: 0.1.0.
Current technical-pilot scoring uses equal-weight hidden behavioral cases with a normalized score.

The older proposed 60/20/20 weighting is not implemented.

The current grader is suitable for trusted/internal pilot use, not as a hardened hostile-code sandbox.

## Provenance
New participants freeze protocol, learning module, prompt, provider/model where applicable, AI cap, and Supported duration.

Attempts preserve task version, grader version after grading, timestamps, and Supported end reason.

Frozen provenance drives runtime behavior. Historical versions remain resolvable; unknown versions fail closed.

## Pilot stages
### Content/instrument pilot
Approximately 3–5 suitable participants. Purpose: clarity, task interpretation, hidden prerequisites, difficulty, UX, tutor helpfulness/over-helping. Not confirmatory.

### Feasibility pilot
Provisional ~8–15 participants. Purpose: real follow-up completion, attrition, timing, AI usage, technical reliability, floor/ceiling calibration.

### Confirmatory study
Sample size determined prospectively from finalized effect/model assumptions and attrition.

## Analysis direction
Primary confirmatory emphasis remains the Condition × Immediate interaction predicting later unaided outcomes. Exact model, exclusions, missing-data rules, multiplicity, and effect-size definition must be preregistered.

## Ethics
Resolve appropriate consent/ethics requirements before human feasibility/confirmatory collection. Collect only necessary participant data and follow approved withdrawal/data-retention rules.

## Repository/deployment confidentiality
Participants should receive only the participant-facing deployment URL and participant code.

Because the repository exposes research design and grader implementation, do not use the GitHub repository as participant material. Protect researcher-only grader specifications before confirmatory collection.

## Scope boundary
Do not add RAG, adaptive learning, personalization, multi-subject infrastructure, dashboards, gamification, recommendation systems, or automated reminder infrastructure to this study unless the research design is deliberately revised.
