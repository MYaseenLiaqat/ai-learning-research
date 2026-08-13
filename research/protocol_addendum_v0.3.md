# Research Protocol Addendum v0.3

## Experimental comparison
Active-control randomized comparison:

**No-AI:** standardized programming learning module.

**AI:** identical module plus controlled generative-AI assistance.

The control group is not deprived of instruction.

## Sequence
1. Eligibility/prerequisite screen
2. Standardized explanation
3. Worked example
4. Guided practice
5. Static hints
6. Supported experimental task
7. AI disabled for everyone
8. Immediate Independent assessment
9. Approximately 7-day Delayed assessment
10. Transfer assessment
11. Approximately 21-day Criterion assessment

## Assignment
Randomize participants to AI or NO_AI before the supported learning phase. Concept order should be counterbalanced/randomized according to a predeclared schedule.

## AI treatment
Pilot settings:
- 20-minute supported phase
- maximum 8 AI requests

These are provisional and must be calibrated in the pilot.

AI may explain, hint, debug, suggest code, or provide complete solutions. The model/configuration/system prompt must be frozen before confirmatory collection.

## AI logging
Store participant ID, condition, concept, task, request sequence, timestamp, prompt, response, request count, and phase. No cross-task memory or personalization.

## Independent assessments
Backend must reject AI access during Immediate, Delayed, Transfer, and Criterion stages.

## Primary outcomes
1. Immediate Independent score
2. Delayed Retention score
3. Transfer score

Criterion is secondary until the final analysis plan is locked.

## Grading
Behavioral hidden tests. Recommended weighting:
- 60% core behavior
- 20% boundary/edge behavior
- 20% input/output contract

No primary-outcome points for style.

## Pilot
Approximately 8–10 participants. Use pilot data for feasibility, task calibration, timing, grader validation, AI-budget calibration, and attrition assessment—not confirmatory treatment claims.

## Power
Do not lock the final sample size yet. After pilot calibration, use simulation incorporating reliability, Immediate-to-Delayed correlation, expected condition effect, expected condition×Immediate interaction, repeated observations, and attrition.

## Analysis direction
Candidate mixed-effects model:

Outcome ~ Condition + Immediate + Condition×Immediate + PriorAbility + Concept + Difficulty + (1|Participant)

The exact model, missing-data rules, exclusion rules, and multiplicity handling must be preregistered before confirmatory collection.

## Data integrity
Version and timestamp the learning material, task, grader, AI model/configuration, and system prompt.

## Ethics
Before human pilot/confirmatory collection, establish the appropriate institutional consent/ethics process. Collect only necessary participant information and support withdrawal/data-deletion requirements where applicable.
