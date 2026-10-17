"""Tests for health_check MCP tool."""

import pytest

from cautious_dollop.server import create_server


@pytest.fixture
def server():
    return create_server()


@pytest.mark.asyncio
async def test_health_check_returns_ok(server):
    result = await server.call_tool("health_check", {})
    assert result.structured_content["status"] == "ok"


@pytest.mark.asyncio
async def test_health_check_returns_service_name(server):
    result = await server.call_tool("health_check", {})
    assert result.structured_content["service"] == "cautious-dollop"


@pytest.mark.asyncio
async def test_health_check_returns_version(server):
    result = await server.call_tool("health_check", {})
    assert result.structured_content["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_health_check_response_schema(server):
    result = await server.call_tool("health_check", {})
    data = result.structured_content
    assert isinstance(data, dict)
    assert "status" in data
    assert "service" in data
    assert "version" in data
    assert len(data) == 3


@pytest.mark.asyncio
async def test_health_check_no_error(server):
    result = await server.call_tool("health_check", {})
    assert result.is_error is False
