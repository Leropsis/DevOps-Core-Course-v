from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_root_endpoint_structure():
    response = client.get("/", headers={"User-Agent": "pytest"})
    assert response.status_code == 200

    data = response.json()
    assert data["service"]["name"] == "devops-info-service"
    assert data["service"]["framework"] == "FastAPI"

    assert "hostname" in data["system"]
    assert "platform" in data["system"]
    assert isinstance(data["system"]["cpu_count"], int)

    assert isinstance(data["runtime"]["uptime_seconds"], int)
    assert "current_time" in data["runtime"]

    assert data["request"]["method"] == "GET"
    assert data["request"]["path"] == "/"

    endpoints = {item["path"] for item in data["endpoints"]}
    assert "/" in endpoints
    assert "/health" in endpoints


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert isinstance(data["uptime_seconds"], int)
    assert isinstance(data["timestamp"], str)


def test_unknown_endpoint_returns_404():
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"
