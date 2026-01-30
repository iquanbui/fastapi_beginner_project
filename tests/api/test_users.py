from fastapi.testclient import TestClient
from app.core.config import settings


def test_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_login_access_token(client: TestClient):
    # Dùng form-data cho OAuth2 login (phải đúng format username/password)
    login_data = {
        "username": "test@example.com",
        "password": "password123",
    }
    response = client.post(f"/login", data=login_data)
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"


def test_read_users_me(client: TestClient):
    # 1. Login lấy token
    login_data = {
        "username": "test@example.com",
        "password": "password123",
    }
    r_login = client.post(f"/login", data=login_data)
    token = r_login.json()["access_token"]

    # 2. Gọi API bảo vệ kèm Header Authorization
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/users/1", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
