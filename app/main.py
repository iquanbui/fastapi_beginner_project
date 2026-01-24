from app.api.endpoints import users
from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# Include routers

app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Beginner Project!"}
