from app.api.endpoints import users
from fastapi import FastAPI
from app.core import config

app = FastAPI(title=config.PROJECT_NAME, version=config.PROJECT_VERSION)

# Include routers

app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Beginner Project!"}
