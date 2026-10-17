"""Tests for echo MCP tool."""

import pytest
from fastmcp.exceptions import ValidationError

from cautious_dollop.server import create_server


@pytest.fixture
def server():
    return create_server()


@pytest.mark.asyncio
async def test_echo_returns_message(server):
    result = await server.call_tool("echo", {"message": "hello world"})
    assert result.structured_content["message"] == "hello world"


@pytest.mark.asyncio
async def test_echo_returns_same_text(server):
    result = await server.call_tool("echo", {"message": "test message 123"})
    assert result.structured_content["message"] == "test message 123"


@pytest.mark.asyncio
async def test_echo_response_schema(server):
    result = await server.call_tool("echo", {"message": "echo test"})
    data = result.structured_content
    assert isinstance(data, dict)
    assert "message" in data
    assert len(data) == 1


@pytest.mark.asyncio
async def test_echo_empty_string(server):
    result = await server.call_tool("echo", {"message": ""})
    assert result.structured_content["message"] == ""


@pytest.mark.asyncio
async def test_echo_no_error(server):
    result = await server.call_tool("echo", {"message": "test"})
    assert result.is_error is False


@pytest.mark.asyncio
async def test_echo_missing_message_raises(server):
    with pytest.raises(ValidationError):
        await server.call_tool("echo", {})


@pytest.mark.asyncio
async def test_echo_invalid_input_raises(server):
    with pytest.raises(ValidationError):
        await server.call_tool("echo", {"message": 123})
