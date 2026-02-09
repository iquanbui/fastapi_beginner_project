from contextlib import asynccontextmanager
from app.api.endpoints import users, auth
from fastapi import FastAPI, Depends
from app.core.config import settings
from app.core.redis_client import redis_client
import redis.asyncio as redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_client.connect()
    yield
    await redis_client.close()


app = FastAPI(title=settings.PROJECT_NAME,
              version=settings.PROJECT_VERSION, lifespan=lifespan)


@app.get("/redis-health")
async def check_redis(redis: redis.Redis = Depends(redis_client.get_client)):
    try:
        data = await redis.ping()
        return {"redis_status": "connected" if data else "error"}
    except Exception as e:
        return {"redis_status": "error", "message": str(e)}

# Include routers

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, tags=["auth"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Beginner Project!"}
