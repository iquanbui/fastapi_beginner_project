from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from sqlalchemy.orm import Session
from typing import List
import json
from fastapi.encoders import jsonable_encoder
import redis.asyncio as redis
from app.core.redis_client import redis_client

from app.schemas import user as schemas
from app.crud import user as crud
from app.core.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
    redis: redis.Redis = Depends(redis_client.get_client)
):
    # 1. Check Cache
    cache_key = f"user:{user_id}"
    cached_user = await redis.get(cache_key)

    if cached_user:
        return json.loads(cached_user)

    # 2. Cache Miss -> Query DB
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # 3. Set Cache (Expire after 1 hour)
    user_data = jsonable_encoder(db_user)
    await redis.set(cache_key, json.dumps(user_data), ex=3600)

    return db_user


@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
    redis: redis.Redis = Depends(redis_client.get_client)
):
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Invalidate Cache
    cache_key = f"user:{user_id}"
    await redis.delete(cache_key)

    return db_user


@router.delete("/{user_id}", response_model=schemas.User)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
    redis: redis.Redis = Depends(redis_client.get_client)
):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Invalidate Cache
    cache_key = f"user:{user_id}"
    await redis.delete(cache_key)

    return db_user
