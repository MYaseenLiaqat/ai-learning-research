# Loops Instrument Audit v0.1

## Decision
The Loops module is suitable for pilot implementation after the controls below are applied.

## Construct
Conditional iteration over a sequence while maintaining or constructing a result.

## Internal-validity controls
Both conditions receive identical:
- concept explanation
- worked example
- guided practice
- static hints
- supported task
- time limit
- programming environment
- grading

Only AI availability differs.

## Assessment validity
- Immediate: changed context and threshold boundary.
- Delayed: changes output from count to conditional sum.
- Transfer: changes output from scalar aggregation to filtered-list construction.
- Criterion: novel context and wording; final version must not reuse earlier values.

## Prerequisites
Variables, assignment, comparisons, if-statements, basic lists, basic Python syntax.

## Pilot calibration
Measure completion time, correctness, error types, perceived difficulty, ceiling/floor effects, and grader behavior. Replace tasks with obvious ceiling/floor problems before confirmatory collection.

## AI exposure
Log request count, request type, prompt, response, timestamps, and subsequent submissions. Primary analysis remains intention-to-treat by randomized condition.

## AI lockout
AI must be disabled server-side during Immediate, Delayed, Transfer, and Criterion assessments.

## Evidence
A 2025 randomized controlled trial reported lower 45-day retention after unrestricted ChatGPT-assisted study than traditional study, supporting delayed unaided assessment as an important outcome. Another 2025 programming study reported that complete GenAI solutions can improve task performance without consistently producing knowledge gains. An exploratory 2025 programming study found frequent requests for complete solutions, supporting detailed interaction logging.

## Conclusion
Proceed to pilot implementation, but do not begin confirmatory collection until task variants, AI configuration, grading, randomization, consent/eligibility, and power analysis are frozen.
