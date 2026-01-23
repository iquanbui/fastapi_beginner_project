from fastapi import FastAPI
from app.core import config

app = FastAPI(title=config.PROJECT_NAME, version=config.PROJECT_VERSION)

# Include routers
# app.include_router(router, prefix="/api/v1/resource", tags=["resource"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Beginner Project!"}
