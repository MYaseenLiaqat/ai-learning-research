from fastapi import FastAPI
from app.db import init_db
from app.routers import health, learners, tasks, ai

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
