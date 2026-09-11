# Loops Task Instrument v0.5.0

## Status

Current transferable loop-problem-solving assessment instrument.

Runtime task version: `0.5.0`.

## Construct and contract

Tasks use variables, assignment, `for`, `if/else`, comparisons, simple lists/strings, counters, accumulators, simple arithmetic, and `result`. The platform provides the input variable. Learners must not redefine it. Hidden tests and expected values are researcher-only.

## Stages

### Supported - counting task

Input: `temperatures`. Set `result` to the number of temperatures strictly greater than 30.

Purpose: learning and practice.

### Immediate - different counting context

Input: `scores`. Set `result` to the number of scores greater than or equal to 50.

Purpose: immediate unaided mastery in a changed context.

### Delayed - retention counting task

Input: `ages`. Set `result` to the number of ages strictly less than 18.

Purpose: retention of the counting construct.

### Transfer - maximum tracking

Input: `scores`. Set `result` to the largest score in the provided list. The approved task contract defines the empty-list behavior.

Purpose: transfer the loop reasoning framework to maximum tracking.

### Criterion - multiple state variables

Input: `activity`, a list containing simple strings such as `"yes"` and `"no"`. Set `result` to the length of the longest consecutive streak of `"yes"` values. The solution requires a current-streak state and a best-streak state, with `if/else` updates.

Purpose: unseen, more complex application requiring multiple state variables.

## Grading

All tasks use execution-based grading with `result_var: "result"`, hidden normal, empty, boundary, duplicate, and edge cases appropriate to each stage. The public instrument does not reproduce expected values. Scoring remains equal-weight hidden behavioral cases normalized by grader version `0.1.0`.

## Timing

- Supported: Day 0
- Immediate: after Supported
- Delayed: approximately +7 days
- Transfer: approximately +14 days
- Criterion: approximately +21 days
