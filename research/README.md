# Research documentation map

The main professor-facing research document is
[docs/RESEARCH.md](../docs/RESEARCH.md). It summarizes the current design,
implementation, intervention, measurements, provenance, limitations, and
planned phases.

## Document locations

- `docs/RESEARCH.md` — current integrated research design and project
  documentation.
- `research/` — current active research documentation and implementation
  specifications.
- `research/archive/` — historical or superseded versions retained for
  traceability; their contents are not rewritten.

## Current authoritative documents

| Document | Role |
|---|---|
| [protocol_v0.4.md](protocol_v0.4.md) | Current content-pilot protocol and analysis direction |
| [loops_learning_module_v0.6.md](loops_learning_module_v0.6.md) | Current Python loops learning specification |
| [loops_task_instrument_v0.5.0.md](loops_task_instrument_v0.5.0.md) | Current staged task and timing instrument |
| [ai_tutor_policy_v0.6.md](ai_tutor_policy_v0.6.md) | Current Controlled-AI treatment policy |
| [loops_prerequisite_screener_v0.3.md](loops_prerequisite_screener_v0.3.md) | Readiness and prerequisite screening |
| [pilot_protocol_clarification_v0.3.md](pilot_protocol_clarification_v0.3.md) | Pilot timing and implementation clarification |
| [loops_instrument_audit_v0.2.md](loops_instrument_audit_v0.2.md) | Current instrument audit record |
| [SCOPE.md](SCOPE.md) | Explicit project boundary and excluded features |
| [CHANGELOG.md](CHANGELOG.md) | Documentation and protocol change history |

The backend is the runtime authority for defaults and registries. In
particular, the current configuration uses protocol `v0.4`, learning module
`v0.6.0`, system prompt `0.6.0`, Groq model
`llama-3.1-8b-instant`, an eight-interaction cap, and a 20-minute Supported
phase. Seeded tasks use instrument version `0.5.0`; the grader reports version
`0.1.0`.

## Version families

Protocol, learning module, task instrument, system prompt, grader, and screener
versions are independent. They do not need matching numbers. Historical
documents in `archive/` are evidence of earlier decisions and should not be
rewritten to match current runtime behavior.
