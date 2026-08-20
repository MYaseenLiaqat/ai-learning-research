from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.db import init_db
from app.routers import health, learners, tasks, ai, learning

app = FastAPI(
    title="AI Learning Measurement Platform",
    version="0.1.0",
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(health.router)
app.include_router(learners.router, prefix="/learners", tags=["learners"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(ai.router, prefix="/ai", tags=["controlled-ai"])
app.include_router(learning.router, prefix="/learning", tags=["learning"])

# Serve the participant-facing frontend (static files).
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(FRONTEND_DIR / "index.html")
