# Loops Instrument Audit v0.2

## Status
Current pre-content-pilot audit for protocol v0.4.

## Decision
The current Loops instrument is suitable for a small content/instrument pilot, subject to the deployment and calibration cautions below.

It is not yet a locked confirmatory instrument.

## Target construct
Basic conditional iteration:

`INITIALIZE → ITERATE → CHECK → UPDATE → RESULT`

The instrument focuses on maintaining a scalar result through counting, summation, and transformed accumulation.

## Prerequisite control
Required prerequisites are limited to variables/assignment, simple lists, comparisons, `if`, indentation, and basic arithmetic/simple Python syntax.

The prerequisite screener avoids directly teaching/testing Loops as the target concept.

## Learning-material validity
Learning module v0.4.0 improves earlier versions by:
- teaching one-value-at-a-time execution;
- tracing True/False conditions;
- explaining why counting starts at zero;
- distinguishing `result += 1` from `result += value`;
- using dry runs and guided practice.

## Internal-validity control
Both conditions receive identical learning material, worked examples, guided practice, static hints, Supported task, timing, environment, and grading.

Only controlled-AI participants receive the tutor during Supported.

AI is blocked server-side during independent assessments.

## Task validity
Supported: conditional counting.

Immediate: changed-context/boundary conditional counting.

Delayed: conditional summation.

Transfer: transformed conditional accumulation. This improves the older filtered-list Transfer by removing `append`/list-construction as an undeclared prerequisite.

Criterion: conditional summation in a shift-hours context with less scaffolded wording. Version 0.3.1 fixes the earlier “overtime hours” ambiguity.

## Participant clueing
Current prompts do not display expected results or hidden grading cases.

Independent assessments provide neutral submission acknowledgement rather than correctness feedback.

## AI treatment validity
Prompt 0.3.0 is learner initiated and pedagogically constrained.

It allows direct conceptual explanation, tracing, hints, and analogous examples, while prohibiting complete active-task solutions, adaptive/automatic intervention, research-hypothesis disclosure, and hidden grader disclosure.

## Timing
Full schedule:
- Day 0 Learning + Supported + Immediate
- approximately Day 7 Delayed
- approximately Day 14 Transfer
- approximately Day 21 Criterion

Manual reminders are acceptable for the small pilot if standardized and instruction-free.

## Grading
Current grader is behavior-based, uses an execution/result contract, multiple hidden cases, equal-weight technical-pilot scoring, and versioned grader metadata.

The older 60/20/20 proposal is not implemented.

## Provenance
The implementation freezes study protocol, learning module, system prompt, provider/model, AI cap, and Supported duration. Attempts preserve task/grader versions and timing.

Historical prompt/module versions remain resolvable.

## Remaining risks
- tutorial difficulty may not fit the target population;
- Supported/Immediate may show ceiling effects;
- Transfer may still be interpreted inconsistently;
- Criterion remains conceptually close to Delayed summation;
- model outputs may occasionally approach the no-solution boundary;
- 20 minutes / 8 interactions remain provisional;
- grader execution is trusted/internal, not a hardened hostile-code sandbox;
- a public repository can expose hypotheses and code-level grader cases.

## Deployment safeguard
Do not give participants the GitHub repository URL.

Before feasibility/confirmatory collection, researcher-only grader specifications and treatment details should not be reasonably discoverable from the participant-facing deployment.

If the repository stays public, protect or relocate hidden grader cases before confirmatory data collection.

## Recommendation
Proceed to a 3–5-person content/instrument pilot to evaluate clarity, interpretation, difficulty, hidden prerequisites, tutor helpfulness/over-helping, and UX.

Do not use that sample for confirmatory causal claims.

After repeated problems are resolved, freeze the instrument before a real feasibility pilot.
