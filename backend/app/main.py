from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.projects import router as projects_router
from app.api.tasks import router as tasks_router
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(title="TaskFlow API")

app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(tasks_router)

@app.get("/")
async def root():
    return {"message": "Welcome to TaskFlow API"}
