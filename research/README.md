# AI-Assisted Learning Research — Research Documentation Index

## Purpose
This folder contains historical and current research specifications for the AI-assisted programming-learning study. The application is a research instrument, not a general learning platform. See `SCOPE.md`.

## Current pilot source of truth

| Artifact | Current version | Source |
|---|---:|---|
| Study protocol | v0.4 | `protocol_v0.4.md` |
| Loops learning module | v0.4.0 | `loops_learning_module_v0.4.md` + backend registry |
| Loops task instrument | 0.4.0 | `loops_task_instrument_v0.4.0.md` + `backend/scripts/seed.py` |
| AI tutor policy | v0.3 / prompt 0.3.0 | `ai_tutor_policy_v0.3.md` + backend registry |
| Prerequisite screener | v0.3 | `loops_prerequisite_screener_v0.3.md` |
| Pilot timing clarification | v0.3 | `pilot_protocol_clarification_v0.3.md` |
| Instrument audit | v0.2 | `loops_instrument_audit_v0.2.md` |
| Grader | 0.1.0 | backend grader implementation |

Older files remain historical evidence and must not be rewritten to reflect later decisions.

## Protocol chronology
- v0.1: `protocol_v0.1.md`
- v0.2 stage: `research_design_v0.2.md`
- v0.3 stage: `protocol_addendum_v0.3.md` plus v0.3 pilot clarifications
- v0.4: `protocol_v0.4.md`

Separate v0.2/v0.3 protocol files are not fabricated because those stages were already represented by the artifacts above.

## Historical reconstruction policy
Some runtime versions existed before matching Markdown specifications. Reconstructed files are explicitly labeled **Historical reconstruction** and must describe only behavior supported by repository history.

## Independent version families
Protocol, learning module, task instrument, system prompt, grader, and screener versions are independent. They do not need matching numbers.

Current combination:
- protocol v0.4
- learning module v0.4.0
- task instrument 0.4.0
- system prompt 0.3.0
- grader 0.1.0
- screener v0.3

## Participant-facing confidentiality
Do not give participants the GitHub repository URL. The repository contains research hypotheses and grader implementation details.

Before feasibility or confirmatory collection, participant-facing deployment must not expose researcher-only grader cases, system prompts, hypotheses, or condition-assignment details.

## Data separation
Keep development/smoke, content-pilot, feasibility-pilot, and confirmatory databases separate.

Never commit:
- `research.db` or backups
- `.env` or API keys
- virtual environments
- identifiable participant exports

## Status
Current documentation target: protocol v0.4 content-pilot freeze.
