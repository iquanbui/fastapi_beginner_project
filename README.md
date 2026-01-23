# FastAPI Beginner Project

Đây là cấu trúc dự án mẫu dành cho người mới bắt đầu với FastAPI.

## Cài đặt

1. Tạo môi trường ảo (khuyến khích):

    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

2. Cài đặt các thư viện:

    ```bash
    npm install # (Nếu bạn dùng nodejs, nhưng đây là python)
    pip install -r requirements.txt
    ```

## Chạy ứng dụng

Chạy lệnh sau từ thư mục gốc `fastapi_beginner_project`:

```bash
uvicorn app.main:app --reload
```

## Cấu trúc thư mục

* `app/main.py`: Điểm khởi chạy của ứng dụng.
* `app/api/endpoints/`: Chứa các endpoint API (logic xử lý).
* `app/schemas/`: Chứa các Pydantic models (dữ liệu đầu vào/ra).
* `app/core/`: Cấu hình chung của dự án.
* `app/models/`: Chứa các model tương tác với Database (nếu có).

## Sử dụng

Mở trình duyệt và truy cập: `http://127.0.0.1:8000/docs` để xem Swagger UI.

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
