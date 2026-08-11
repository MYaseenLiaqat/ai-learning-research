# AI Learning Measurement Platform v0.1

Minimal research instrument for the AI-in-education experiment.

Implements:
- FastAPI task server
- SQLAlchemy persistence
- learner randomization
- measurement arms
- delayed scheduling
- sandboxed Python grading with fixed tests
- controlled AI condition with fixed prompt and interaction cap
- AI interaction audit logging

This is a research prototype, not a production participant platform.

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/seed.py
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

Set `DATABASE_URL` for PostgreSQL. SQLite is the default for local development.

For AI, set `LLM_BASE_URL`, `LLM_API_KEY`, and `LLM_MODEL`.
