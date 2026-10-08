# Loops Task Instrument v0.4.0

## Status

Current Loops feasibility/content-pilot assessment instrument.

Runtime task version: `0.4.0`.

## Construct and contract

The instrument measures basic conditional iteration while maintaining scalar state. The platform provides the input variable. The learner must not redefine it and assigns the final answer to `result`. Hidden tests and expected values are researcher-only. AI is unavailable during independent assessments.

## Stages and purposes

### Supported - counting task

Input: `temperatures`. Count values strictly greater than 30.

Purpose: learning and practice with the assigned condition during Supported.

### Immediate - counting task

Input: `scores`. Count values greater than or equal to 50.

Purpose: immediate unaided mastery of the counting construct in a changed context and threshold form.

### Delayed - counting task in a different context

Input: `ages`. Count values less than 18.

Purpose: retention of the same counting construct in a different context.

### Transfer - summation task

Input: `prices`. Add the prices strictly greater than 1000.

Purpose: apply the learned reasoning to a related but different summation problem, requiring an accumulator instead of a counter.

### Criterion - multi-state application

Input: `transactions`. For each transaction at least 100, increment a counter and add the transaction value to an accumulator. Set `result` to the sum of qualifying transaction values. The task requires reasoning about both a counter and an accumulator, while remaining within the approved loop construct.

Purpose: more complex independent application requiring multiple state variables.

## Grading specifications

All tasks use execution-based grading with `result_var: "result"`. Each task has hidden behavioral cases covering normal, empty, boundary, duplicate, all-qualifying, and no-qualifying inputs as appropriate. The public instrument does not reproduce expected values.

Current scoring is equal-weight hidden behavioral cases normalized by the grader. The grader version remains `0.1.0`.

## Timing

- Supported: Day 0
- Immediate: after Supported
- Delayed: approximately +7 days
- Transfer: approximately +14 days
- Criterion: approximately +21 days

## Instrument controls

Task wording must preserve the provided-input contract, avoid expected-answer leakage, and remain within variables, assignment, comparisons, `if`, `for`, counters, accumulators, simple arithmetic, and `result`.
