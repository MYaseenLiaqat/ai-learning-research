# AI Learning Research — Research Design v0.2

## Status

Working research-design specification. This document supersedes the concept-selection portion of protocol v0.1 but does **not** yet constitute the final preregistration/protocol lock.

## 1. Research question

Does AI assistance change the relationship between students' immediate independent programming performance and subsequent unaided learning outcomes, specifically delayed retention and transfer?

Primary statistical focus:

`Delayed/Transfer outcome ~ Immediate independent performance + AI condition + Immediate × AI`

The central contribution is the interaction/moderation question, not simply whether AI improves average performance.

## 2. Experimental domain

Python programming is retained as the controlled test domain because it permits objective, reproducible grading, controlled task difficulty, and construction of retention and transfer tasks.

## 3. Concept selection

### Primary concepts

1. Iteration / loops
2. Functions / abstraction
3. Dictionary-based data representation

### Excluded from the primary experiment

- Recursion: excluded because of substantially higher conceptual difficulty and greater risk that floor effects dominate the learning measure.
- Lists as a standalone concept: treated as prerequisite/supporting knowledge rather than an independent experimental construct because list operations are tightly entangled with iteration in many natural Python tasks.

This decision should be revisited only if pilot evidence shows a construct problem.

## 4. Prerequisite knowledge

Participants should have basic Python familiarity sufficient to understand:

- variables
- numeric/string/boolean values
- assignment
- comparison operators
- `if` statements
- basic lists
- basic input/output
- reading simple Python code

These are measured/controlled as prerequisite knowledge rather than primary experimental concepts.

## 5. Difficulty policy

Tasks should be moderate in conceptual difficulty.

We do not want an easy-to-hard staircase because increasing difficulty would become a confound.

Target characteristics:

- conceptual demand: moderate
- syntax burden: low to moderate
- reasoning steps: approximately 3–5
- short enough to complete without excessive fatigue
- objective automated grading
- meaningful opportunity for AI assistance
- low ceiling risk
- low floor risk
- enough structural variation to prevent memorization

Difficulty should be pilot-calibrated rather than assumed from code length.

## 6. Measurement sequence

Each concept follows:

`Supported → Immediate Independent → Delayed Retention → Transfer → Criterion`

### Supported

The learning/support phase. AI condition receives controlled AI assistance; No-AI condition receives no AI assistance.

### Immediate Independent

AI is unavailable to all participants. Measures immediate unaided performance after the supported phase.

### Delayed Retention

AI unavailable. Same underlying construct after approximately 7 days.

### Transfer

AI unavailable. Same underlying construct but materially changed surface form/problem structure.

### Criterion

AI unavailable. A novel problem requiring independent application of the construct. Target timing approximately 21 days; exact timing remains provisional until protocol lock.

## 7. Task equivalence

Every measurement stage should have multiple parallel task variants.

Variants should preserve:

- construct
- approximate reasoning steps
- input/output complexity
- prerequisite demands
- grading structure

while changing:

- context
- values
- names
- surface wording
- irrelevant narrative details

No participant should receive a memorized copy of an earlier task.

## 8. AI condition

The treatment is a controlled AI-assistance condition.

Working recommendation:

- one fixed system prompt
- one fixed model/version for the study
- fixed interaction budget
- no cross-task memory
- no personalization
- all interactions logged
- AI may explain, debug, provide hints, or provide code unless the final protocol explicitly restricts these behaviors
- AI availability ends before every independent assessment

The interaction budget and exact system prompt remain protocol-lock items.

## 9. Primary outcomes

Primary outcomes:

- immediate independent score
- delayed retention score
- transfer score

Criterion score is a longer-term secondary/validation outcome unless the final statistical analysis specifies otherwise.

Scores should be continuous where possible, based on hidden tests and a predefined rubric.

## 10. Grading

All programming tasks should have:

- visible example input/output where pedagogically appropriate
- hidden test cases
- edge-case test cases
- deterministic execution
- time/resource limits
- no network access
- isolated execution environment
- predefined partial-credit rubric

The grader must evaluate behavior, not code style.

## 11. Randomization

Working recommendation:

- randomize AI vs No-AI condition at participant level before the learning phase
- counterbalance concept order
- randomize equivalent task variants within each concept/stage

The final randomization unit and stratification variables remain protocol-lock items.

## 12. Pilot

Before a confirmatory study:

- approximately 8–10 participants
- test task clarity
- completion time
- ceiling/floor effects
- grader correctness
- AI interaction burden
- scheduling
- delayed completion feasibility
- transfer-task interpretation

Pilot data should be used primarily for feasibility and task calibration, not for claiming confirmatory treatment effects.

## 13. Power

Do not use the old 150–250 estimate as a final requirement.

A preliminary simulation for a modest interaction (roughly a 0.20 standardized change in the Immediate → Delayed slope) indicates that 80–120 participants would be underpowered for a confirmatory interaction test under plausible noise assumptions. Therefore:

- 80–120 may be appropriate for a feasibility/pilot study if recruitment is limited.
- The final confirmatory sample must be determined by an a priori simulation using the finalized task reliability, expected correlation structure, interaction effect, attrition, and repeated-measures structure.

## 14. Analysis

Candidate final model:

`Outcome ~ Immediate + AI + Immediate×AI + PriorAbility + Difficulty + Exposure + TestingDose`

Because participants contribute repeated observations across concepts, the final analysis should use an appropriate mixed-effects/multilevel model with participant-level repeated measures rather than treating every concept observation as independent.

The exact model, missing-data strategy, effect-size definition, and multiplicity handling must be preregistered before confirmatory data collection.

## 15. Current decision

The project should now move from concept selection into task-bank construction and pilot calibration.

Do not build a polished frontend or additional AI infrastructure until the task bank, AI protocol, grading specifications, timing, and randomization are locked.
