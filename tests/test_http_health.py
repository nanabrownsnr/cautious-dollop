"""Tests for HTTP health endpoint."""

import pytest
from starlette.testclient import TestClient

from cautious_dollop.server import create_server


@pytest.fixture
def client():
    server = create_server()
    app = server.http_app()
    return TestClient(app)


def test_health_returns_200(client):
    resp = client.get("/health")
    assert resp.status_code == 200


def test_health_returns_json(client):
    resp = client.get("/health")
    data = resp.json()
    assert isinstance(data, dict)


def test_health_returns_status_ok(client):
    resp = client.get("/health")
    assert resp.json()["status"] == "ok"


def test_health_returns_service_name(client):
    resp = client.get("/health")
    assert resp.json()["service"] == "cautious-dollop"


def test_health_returns_version(client):
    resp = client.get("/health")
    assert resp.json()["version"] == "0.1.0"


def test_health_response_schema(client):
    resp = client.get("/health")
    data = resp.json()
    assert "status" in data
    assert "service" in data
    assert "version" in data
    assert len(data) == 3
