"""Tests for application startup."""

import asyncio

from starlette.testclient import TestClient

from cautious_dollop.app import build_app
from cautious_dollop.server import create_server


def test_build_app_returns_starlette_app():
    app = build_app()
    assert app is not None
    assert hasattr(app, "routes")
    assert hasattr(app, "lifespan")


def test_create_server_returns_fastmcp():
    server = create_server()
    assert server is not None
    assert server.name == "cautious-dollop"


def test_create_server_has_all_tools():
    server = create_server()

    async def check_tools():
        tools = await server.list_tools()
        return [t.name for t in tools]

    tools = asyncio.run(check_tools())
    assert "health_check" in tools
    assert "echo" in tools
    assert "server_info" in tools


def test_http_app_health_endpoint_accessible():
    app = build_app()
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_server_version():
    server = create_server()
    assert server.version == "0.1.0"
