# Loops Task Instrument 0.2.0

## Status
**Historical reconstruction.**

Reconstructed on 2026-09-08 from repository history.

## Runtime version
`0.2.0`

## Main change from 0.1.0
The platform-provided-input contract became explicit.

Prompts stated that the platform already provided the named input variable and instructed the learner not to redefine it. The final answer still had to be assigned to `result`.

## Stage design

| Stage | Historical task form |
|---|---|
| Supported | Conditional count |
| Immediate | Conditional count with changed context/boundary |
| Delayed | Conditional sum |
| Transfer | Filtered-list construction |
| Criterion | Conditional transaction sum |

Expected-result text was still participant-visible at this version.

Transfer still depended on filtered-list construction.

## Grading
Execution-based `result` grading continued with multiple behavioral cases.

Exact cases are not reproduced here.

## Supersession
Version 0.3.0 removed participant-visible expected-result clueing, replaced filtered-list Transfer, and changed Criterion context.
