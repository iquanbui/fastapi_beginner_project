# FastAPI Beginner Project

Đây là cấu trúc dự án mẫu dành cho người mới bắt đầu với FastAPI.

## Cài đặt

1.  Tạo môi trường ảo (khuyến khích):
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

2.  Cài đặt các thư viện:
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

*   `app/main.py`: Điểm khởi chạy của ứng dụng.
*   `app/api/endpoints/`: Chứa các endpoint API (logic xử lý).
*   `app/schemas/`: Chứa các Pydantic models (dữ liệu đầu vào/ra).
*   `app/core/`: Cấu hình chung của dự án.
*   `app/models/`: Chứa các model tương tác với Database (nếu có).

## Sử dụng

Mở trình duyệt và truy cập: `http://127.0.0.1:8000/docs` để xem Swagger UI.
