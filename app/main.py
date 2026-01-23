from fastapi import FastAPI
from app.api.endpoints import projects
from app.core import config

app = FastAPI(title=config.PROJECT_NAME, version=config.PROJECT_VERSION)

# Include routers
app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Beginner Project!"}
