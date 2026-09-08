# Loops Task Instrument 0.3.1

## Status
Current Loops pilot task instrument.

## Runtime version
`0.3.1`

## Construct
Basic conditional iteration over a sequence while maintaining a scalar result.

The task set measures:
- conditional counting;
- conditional summation;
- transformed conditional accumulation;
- independent application in a changed context.

It does not require filtered-list construction.

## Shared participant contract
For every stage:
- the platform provides the input variable;
- the participant must not redefine that input;
- the final answer is assigned to `result`;
- prompts do not show expected results;
- hidden grading cases are not shown;
- AI is unavailable in every independent assessment.

## Stages

### Supported — conditional counting
Input: `temperatures`.
Task: set `result` to the number strictly greater than 30.
AI is available only to controlled-AI participants during active Supported.

### Immediate — independent counting
Input: `scores`.
Task: set `result` to the number greater than or equal to 50.

Purpose: immediate unaided reconstruction with changed context and threshold boundary.

### Delayed — conditional summation
Input: `prices`.
Task: set `result` to the total price strictly more than 1000.

Purpose: retention while changing the accumulator from count to sum.

### Transfer — transformed accumulation
Input: `readings`.
Task: for readings above 30, accumulate how much each exceeds 30.

Purpose: condition + transformation + accumulation without list construction.

### Criterion — less-scaffolded summation
Input: `hours`.
A long shift is defined as lasting at least 10 hours. The learner sets `result` to total hours worked across all long shifts, or 0 if none qualify.

Purpose: longer-term independent application in a new context without ambiguous “overtime” wording.

## Grading
Mode: execution-based `result` grading.

Each stage uses multiple hidden behavioral cases, including appropriate normal, empty, boundary, duplicate, all-qualifying, and no-qualifying conditions.

Exact hidden cases and researcher-only expected values are not reproduced in this public document.

Current grader version: `0.1.0`.

Current pilot scoring: equal-weight hidden cases, normalized by the grader.

The older proposed 60/20/20 weighting is not active.

## Timing
- Supported: Day 0
- Immediate: Day 0 after Supported completes/expires
- Delayed: approximately +7 days
- Transfer: approximately +14 days
- Criterion: approximately +21 days

## Change from 0.3.0
Only Criterion wording changed:
- removed ambiguous “overtime hours”;
- defined “long shift”;
- asked for total hours across qualifying shifts.

Underlying grading behavior and construct were preserved.
