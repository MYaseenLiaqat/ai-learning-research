# Cline Implementation Brief — Research Platform MVP

## Do not redesign the research

Implement only the requirements in the approved research documents.

Before changing code:

1. inspect the existing backend
2. inspect current tests
3. inspect `research/protocol_v0.1.md`
4. inspect the latest research-design document
5. report any conflict instead of silently choosing a new research design

## Current engineering goal

Support a research-driven task platform capable of:

- participant registration
- condition assignment
- concept/task retrieval
- task submission
- objective Python grading
- attempt storage
- AI interaction logging
- delayed task scheduling
- criterion scheduling

## Required traceability

Every attempt must be traceable to:

participant → condition → concept → task → task type → score → timestamp → AI exposure

## Research constraints

- AI must be unavailable during Immediate, Delayed, Transfer, and Criterion assessments.
- AI interaction logs must preserve prompt, response, sequence number, and timestamp.
- Do not add personalization.
- Do not add cross-task memory.
- Do not add RAG.
- Do not add vector databases.
- Do not add recommendation engines.
- Do not add dashboards.
- Do not add unnecessary microservices.

## Grading requirements

The Python grader must:

- run in an isolated/sandboxed environment
- have no network access
- enforce execution time/resource limits
- use hidden test cases
- return deterministic scores
- record grading metadata
- prevent participant code from accessing application secrets

## Acceptance tests

At minimum:

1. participant can be created
2. participant receives one valid experimental condition
3. participant receives the correct task
4. AI condition can request assistance
5. No-AI condition cannot request assistance
6. AI interaction is logged
7. submission is graded
8. score is stored
9. immediate assessment cannot access AI
10. delayed assessment can be scheduled
11. transfer assessment can be scheduled
12. criterion assessment can be scheduled
13. invalid task/participant combinations are rejected
14. grader failures are recorded safely without exposing server internals

## Workflow

After implementation:

- run all tests
- inspect the diff
- do not modify research assumptions
- provide a concise change summary
- provide test results
- stop before adding unrelated features

Do not implement the frontend yet unless explicitly requested after the research protocol is locked.
