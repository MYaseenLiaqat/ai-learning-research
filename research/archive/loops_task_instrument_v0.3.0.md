# Loops Task Instrument 0.3.0

## Status
**Historical reconstruction.**

Reconstructed on 2026-09-08 from repository history.

## Runtime version
`0.3.0`

## Main changes from 0.2.0
- Removed participant-visible expected-result text.
- Preserved the platform-provided input + `result` contract.
- Replaced filtered-list Transfer with transformed conditional accumulation.
- Replaced the transaction Criterion with a shift-hours context.

## Stage specification

### Supported
Input: `temperatures`.
Task: set `result` to the number of temperatures strictly greater than 30.

### Immediate
Input: `scores`.
Task: set `result` to the number of scores greater than or equal to 50.
AI unavailable.

### Delayed
Input: `prices`.
Task: set `result` to the total price of products strictly more than 1000.
AI unavailable.

### Transfer
Input: `readings`.
Task: set `result` to the total amount by which readings above 30 exceed 30.
The prompt included a small explanation of how an above-threshold reading contributes its excess.
AI unavailable.

Purpose: conditional iteration plus transformation and accumulation without list construction.

### Criterion
Input: `hours`.
Historical wording asked for the total number of “overtime hours” across shifts lasting at least 10 hours.

The intended grader behavior summed the full hours of qualifying shifts. The wording was potentially ambiguous because “overtime hours” could also mean only hours beyond the threshold.

## Grading
Execution-based `result` grading with multiple hidden behavioral cases.

Exact hidden cases are intentionally not reproduced in this public document.

## Supersession
Version 0.3.1 changed only the Criterion wording while preserving intended construct and grading behavior.
