from typing import Generator, Any
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import app
# Import models để đảm bảo chúng được đăng ký vào Base.metadata
from app.models import user as user_models

# Sử dụng SQLite file riêng cho test để dễ debug
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def db() -> Generator:
    # Tạo bảng trong DB test
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        # Xóa bảng sau khi test xong (nếu muốn sạch sẽ hoàn toàn thì uncomment dòng dưới)
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client(db: Any) -> Generator:
    # Ghi đè dependency get_db để dùng Test DB
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
