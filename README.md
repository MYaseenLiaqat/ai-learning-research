# AI Learning Research

This repository contains a research instrument for studying how AI assistance
during learning affects later unaided retention and transfer.

> **Research question:** How does AI assistance during learning affect
> learners' subsequent unaided retention and transfer of the learned skill?

The secondary question asks whether AI assistance changes the relationship
between immediate independent performance and later unaided learning outcomes.
Programming is the **initial experimental testbed**, not the scope of the
research: programming gives the first study a structured setting with
standardized tasks, objective automated assessment, controlled AI access, and
reproducible conditions.

## Study at a glance

- Learners are randomly assigned to **No-AI** or **Controlled-AI**.
- Both conditions receive the same standardized learning and task sequence.
- The Controlled-AI tutor is learner-initiated and available only during
  Supported learning.
- Immediate, delayed, transfer, and criterion assessments are AI-free.
- The current testbed teaches introductory Python `for`-loop problem solving.
- The current runtime freezes protocol, module, task, prompt, provider/model,
  interaction-cap, and timing provenance for reproducibility.

The current implementation is an internal content/feasibility pilot, not a
confirmatory claim that AI improves learning.

## Start here

Primary research documentation:

- [docs/RESEARCH.md](docs/RESEARCH.md) — current research design, intervention,
  measurements, provenance, limitations, and implementation status.
- [research/README.md](research/README.md) — map of active and historical
  research specifications.

## Repository layout

```text
backend/   FastAPI application, versioned services, seed data, and tests
frontend/  participant-facing application
research/  active research specifications and archived history
docs/      project documentation
analysis/  analysis workspace
```

## Developer setup

The backend is a Python application. From the repository root:

```powershell
cd backend
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

Local settings are stored in .env. API keys, databases, participant exports, and virtual environments are kept out of version control.
