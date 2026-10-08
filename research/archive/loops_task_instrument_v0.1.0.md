# Loops Task Instrument 0.1.0

## Status
**Historical reconstruction.**

Reconstructed on 2026-09-08 from the first seeded Loops pilot implementation. This Markdown file did not exist contemporaneously.

## Construct
Conditional iteration over a sequence while maintaining or constructing a result.

## Runtime version
`0.1.0`

## Stage design

| Stage | Historical task form |
|---|---|
| Supported | Count temperatures above a threshold |
| Immediate | Count scores at/above a threshold |
| Delayed | Sum prices above a threshold |
| Transfer | Construct a filtered list above a threshold |
| Criterion | Sum qualifying transaction values |

## Participant-prompt behavior
At this stage:
- prompts showed the input assignment;
- final answer went to `result`;
- prompts displayed expected results;
- Transfer required filtered-list construction;
- Criterion used a transaction context.

## Grading
Execution-based `result` grading with multiple cases.

Exact historical grading cases are intentionally not reproduced in this public research document.

## Later identified limitations
Participant-visible expected results could clue answers. Filtered-list Transfer introduced list-construction/`append` knowledge outside the intended narrow Loops construct. These issues motivated later revisions.
