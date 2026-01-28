from sqlalchemy.orm import Session
from app.models.user import Users
from app.schemas.user import UserCreate, UserUpdate
from app.core import security


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user


def get_user(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(Users).filter(Users.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Users).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = Users(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = security.get_password_hash(
            update_data.pop("password"))

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
