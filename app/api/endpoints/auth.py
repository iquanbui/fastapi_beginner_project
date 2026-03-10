from jose import jwt
from app.core.redis_client import redis_client
import redis.asyncio as redis
from app.models import user as models
from app.api.deps import oauth2_scheme, get_current_user
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.crud import user as crud
from app.schemas import token as token_schemas
from app.core.database import get_db

router = APIRouter()


@router.post("/login", response_model=token_schemas.Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.email, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme),
    current_user: models.Users = Depends(get_current_user),
    redis_conn: redis.Redis = Depends(redis_client.get_client)
):
    """
    Logout current user by adding token to blacklist
    """
    try:
        # Decode token to get expiration time
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        exp = payload.get("exp")

        # Calculate TTL
        import time
        current_time = int(time.time())

        if exp:
            ttl = exp - current_time
            if ttl > 0:
                # Add to redis blacklist
                await redis_conn.setex(f"blacklist:{token}", ttl, "true")

        return {"message": "Successfully logged out"}

    except Exception as e:
        # Trong trường hợp token lỗi nhưng vẫn vào được đây (hiếm), cứ log ra
        raise HTTPException(status_code=400, detail="Error logging out")
