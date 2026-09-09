# AI Learning Research - Research Design v0.3

## Status

This is a feasibility/content pilot design. It is intended to evaluate task clarity, instructional fit, assessment behavior, tutor policy adherence, timing, and technical feasibility. It is not a confirmatory test of whether AI improves learning, and pilot results will not support causal claims about AI improving learning.

## 1. Experimental domain

The first experimental domain is Python programming, with basic conditional iteration using `for` loops as the first experimental construct. The construct is deliberately narrow so that instruction, task prompts, grading, and tutor assistance can remain controlled and reproducible.

Target constructs:

- variables
- assignment
- comparisons
- `if` statements
- basic `for` loops
- counters
- accumulators
- simple arithmetic
- the `result` variable

The pilot does not require `while`, nested loops, `break`, `continue`, functions, recursion, dictionaries, comprehensions, advanced libraries, or other shortcuts outside the approved construct.

## 2. Conditions

Participants are assigned to one of two participant-level conditions:

- **No-AI:** standardized learning material and Supported practice without generative AI assistance.
- **Controlled-AI:** the same material and task with learner-initiated, pedagogically constrained AI tutoring during Supported practice only.

The conditions, frozen participant provenance, grading, scheduling, and assessment blocking are implementation controls and are not changed by this document.

## 3. Assessment purposes

The sequence is:

`Supported -> Immediate -> Delayed -> Transfer -> Criterion`

- **Supported:** learning and practice with the assigned treatment.
- **Immediate:** immediate unaided mastery of the same core construct.
- **Delayed:** retention of the same construct in another counting task.
- **Transfer:** application of learned reasoning to a related but different summation problem.
- **Criterion:** a more complex application requiring more than one kind of state.

AI is unavailable during all independent assessments.

## 4. Background variables

Collect or characterize relevant background information before or alongside the pilot, including prior Python experience and specifically prior experience writing or reading Python `for` loops. Prior for-loop experience is a background/readiness variable, not a treatment outcome.

Other useful feasibility variables include prior ability, task completion time, interaction count, dropout or missed follow-up, and participant interpretation of instructions.

## 5. Feasibility outcomes

Evaluate:

- whether learners understand the module and input contract;
- completion time and scheduling feasibility;
- floor and ceiling behavior;
- whether the five stages distinguish practice, immediate mastery, retention, transfer, and more complex application;
- grading correctness and hidden-test coverage;
- controlled-AI interaction burden and policy adherence;
- delayed follow-up completion and attrition.

Use pilot data for content and instrument calibration. Do not interpret observed condition differences as causal evidence that AI improves learning.

## 6. Construct limitation

Results from this pilot are specific to basic Python conditional iteration and the selected counting/summation tasks. They should not be generalized to Python programming as a whole, other programming constructs, other subjects, broader AI tutoring, or confirmatory learning effects without additional evidence.

## 7. Provenance and integrity

New learners freeze the protocol, learning material, task, prompt, provider/model where applicable, interaction cap, and Supported duration. Historical versions remain resolvable so frozen participants remain reproducible. No-AI learners have no AI-specific provenance.

Expected answers, hidden tests, grading specifications, and research variables remain researcher-only information.

## 8. Next step

Use the feasibility/content pilot to revise task wording, learning material, tutor policy, timing, and audit criteria before any confirmatory protocol or causal analysis is considered.
