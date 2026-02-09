import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import sys

# Setup logger to stdout
logger = logging.getLogger("api_processor")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        # Log ra console (force flush để hiện ngay trên Docker logs)
        log_message = f"API LOG: Path: {request.url.path} - Method: {request.method} - Time: {process_time:.4f}s"
        print(log_message, flush=True)
        # logger.info(log_message)

        # Thêm header X-Process-Time vào response trả về client
        response.headers["X-Process-Time"] = str(process_time)

        return response
