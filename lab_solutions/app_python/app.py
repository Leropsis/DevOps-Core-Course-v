import os
import logging
import platform
import socket
from datetime import datetime, timezone
from fastapi import FastAPI, Request


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"


logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


logger = logging.getLogger(__name__)


START_TIME = datetime.now(timezone.utc)


app = FastAPI(title="DevOps Info Service", version="1.0.0")


def get_uptime():
    delta = datetime.now(timezone.utc) - START_TIME
    seconds = int(delta.total_seconds())
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return {"seconds": seconds, "human": f"{hours} hours, {minutes} minutes"}


def get_system_info():
    return {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform_version": platform.platform(),
        "architecture": platform.machine(),
        "cpu_count": os.cpu_count() or 0,
        "python_version": platform.python_version(),
    }


def get_request_info(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    return {
        "client_ip": client_ip,
        "user_agent": user_agent,
        "method": request.method,
        "path": request.url.path,
    }


def get_runtime_info():
    now = datetime.now(timezone.utc)
    return {
        "uptime_seconds": get_uptime()["seconds"],
        "uptime_human": get_uptime()["human"],
        "current_time": now.isoformat().replace("+00:00", "Z"),
        "timezone": now.tzname() or "UTC",
    }


@app.get("/")
async def index(request: Request):
    logger.info("Request: %s %s", request.method, request.url.path)
    return {
        "service": {
            "name": "devops-info-service",
            "version": "1.0.0",
            "description": "DevOps course info service",
            "framework": "FastAPI",
        },
        "system": get_system_info(),
        "runtime": get_runtime_info(),
        "request": get_request_info(request),
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Service information"},
            {"path": "/health", "method": "GET", "description": "Health check"},
        ],
    }


@app.get("/health")
async def health():
    now = datetime.now(timezone.utc)
    return {
        "status": "healthy",
        "timestamp": now.isoformat().replace("+00:00", "Z"),
        "uptime_seconds": get_uptime()["seconds"],
    }


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting application on %s:%s", HOST, PORT)
    uvicorn.run(
        "app:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="debug" if DEBUG else "info",
    )
