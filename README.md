# FastAPI Beginner Project

>This is a sample project structure for beginners with FastAPI.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Database & Migration](#database--migration)
- [Testing](#testing)
- [Redis Integration](#redis-integration)
- [Docker Usage](#docker-usage)
- [API Documentation](#api-documentation)

---

## Project Overview
This project demonstrates a basic FastAPI backend with user authentication, database integration, Redis caching, and testing setup.

## Project Structure

```
app/
  main.py            # Application entrypoint
  api/endpoints/     # API endpoints (business logic)
  schemas/           # Pydantic models (request/response)
  core/              # Project-wide configuration
  models/            # Database models
  crud/              # CRUD operations
  ...
alembic/             # Database migrations
tests/               # Pytest test cases
docker-compose.yml   # Docker Compose config
requirements.txt     # Python dependencies
```

## Setup

1. **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On Linux/Mac
    ```
2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

Start the FastAPI server from the project root:
```bash
uvicorn app.main:app --reload
```

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI.

## Hướng dẫn Database & Migration

Phần này hướng dẫn cách tạo bảng trong database thông qua Code (Models) và cập nhật Database (Migrations).

### 1. Cấu hình Database

1. Tạo file `.env` tại thư mục gốc (nếu chưa có) và thêm cấu hình kết nối database.
    Ví dụ cho SQLite (dễ nhất để test):

    ```env
    DATABASE_URL=sqlite:///./sql_app.db
    ```

    Hoặc PostgreSQL:

    ```env
    DATABASE_URL=postgresql://user:password@localhost/dbname
    ```

2. Cấu hình Database Engine đã được thiết lập sẵn tại `app/core/database.py`.
    File này sẽ đọc `DATABASE_URL` từ file `.env` và tạo kết nối.

### 2. Cài đặt thư viện cần thiết

Các thư viện `sqlalchemy`, `alembic` đã được thêm vào `requirements.txt`.
Nếu chưa cài đặt, hãy chạy lại lệnh:

```bash
pip install -r requirements.txt
```

### 3. Tạo Class Model

Tạo một file mới trong thư mục `app/models/`, ví dụ `app/models/user_model.py`.
Class này sẽ đại diện cho một bảng trong Database.

Ví dụ:

```python
from sqlalchemy import Column, Integer, String
from app.core.database import Base # Import Base từ file database.py

class User(Base):
    __tablename__ = "users"  # Tên bảng trong database

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
```

### 3. Chạy Migration (Alembic)

Migration giúp đồng bộ code Python với Database.

#### B1: Khởi tạo Alembic (Chạy 1 lần duy nhất khi bắt đầu dự án)

```bash
alembic init alembic
```

*Lưu ý: Sau bước này cần cấu hình file `alembic.ini` (đường dẫn DB) và `alembic/env.py` (import models).*

#### B2: Tạo file migration (Chạy mỗi khi sửa/thêm model)

Khi bạn tạo mới Class User như trên, hãy chạy lệnh:

```bash
alembic revision --autogenerate -m "them bang users"
```

#### B3: Áp dụng thay đổi vào Database

```bash
alembic upgrade head
```

## Hướng dẫn Testing

Dự án sử dụng `pytest` làm framework kiểm thử chính.
## Database & Migration

### 1. Database Configuration

1. Create a `.env` file in the project root (if not exists) and add your database connection string. Example for SQLite (easy for testing):
    ```env
    DATABASE_URL=sqlite:///./sql_app.db
    ```
    Or for PostgreSQL:
    ```env
    DATABASE_URL=postgresql://user:password@localhost/dbname
    ```
2. The database engine is configured in `app/core/database.py` and reads `DATABASE_URL` from `.env`.

### 2. Migration with Alembic

1. **Initialize Alembic** (run once):
    ```bash
    alembic init alembic
    ```
    > Configure `alembic.ini` (database URL) and `alembic/env.py` (import your models).
2. **Create a migration** (run after modifying/adding models):
    ```bash
    alembic revision --autogenerate -m "create users table"
    ```
3. **Apply migrations:**
    ```bash
    alembic upgrade head
    ```

## Testing

This project uses `pytest` as the main testing framework.

1. **Install test dependencies:** (already in `requirements.txt`)
2. **Run all tests:**
    ```bash
    pytest
    # or
    python -m pytest
    ```
3. **Test configuration:**
    - Config file: `pytest.ini`
    - Test database: A separate `test.db` is created automatically and cleaned up after tests (see `tests/conftest.py`).

## Redis Integration

1. **Configure Redis** in your `.env` file:
    ```env
    REDIS_HOST=localhost
    REDIS_PORT=6379
    REDIS_DB=0
    REDIS_PASSWORD=null
    ```
2. **Start Redis server:**
    - Easiest: use Docker or the provided `docker-compose.yml`:
    ```bash
    docker-compose up -d redis
    ```
3. **Check Redis connection:**
    - Visit: `http://localhost:8000/redis-health`
    - Should return: `{ "redis_status": "connected" }`

## Docker Usage

Run both the backend and Redis with Docker Compose:
```bash
docker-compose up -d --build
```
The API will be available at: [http://localhost:8000](http://localhost:8000)

## Troubleshooting

- **AUTH error:** If you see `AUTH <password> called without any password`, check your `.env` and ensure `REDIS_PASSWORD=null` (or leave blank if no password).
- **Connection error:** Make sure the `redis` container is running (`docker-compose ps`). If running Redis locally (not Docker), ensure Redis server is installed and running on port 6379.

## Linting (flake8)

Code style and linting are enforced using [flake8](https://flake8.pycqa.org/).

### How to Run Linting

1. Make sure flake8 is installed (already included in requirements.txt).
2. To lint the entire project, run:
    ```bash
    python -m flake8 app/
    ```
   Or, if your virtual environment is active:
    ```bash
    flake8 app/
    ```
3. To lint a specific file or folder:
    ```bash
    python -m flake8 app/main.py
    python -m flake8 app/api/
    ```
4. Linting configuration is in the `.flake8` file at the project root.

> Linting errors and warnings will be shown in the terminal. You can also see them directly in VS Code if linting is enabled in your settings.

---

## API Documentation

Interactive API docs are available at:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
