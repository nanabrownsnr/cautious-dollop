"""Tests for server_info MCP tool."""

import pytest

from cautious_dollop.server import create_server


@pytest.fixture
def server():
    return create_server()


@pytest.mark.asyncio
async def test_server_info_returns_service_name(server):
    result = await server.call_tool("server_info", {})
    assert result.structured_content["service"] == "cautious-dollop"


@pytest.mark.asyncio
async def test_server_info_returns_version(server):
    result = await server.call_tool("server_info", {})
    assert result.structured_content["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_server_info_returns_description(server):
    result = await server.call_tool("server_info", {})
    desc = result.structured_content["description"]
    assert isinstance(desc, str)
    assert len(desc) > 0


@pytest.mark.asyncio
async def test_server_info_returns_tools_list(server):
    result = await server.call_tool("server_info", {})
    tools = result.structured_content["tools"]
    assert isinstance(tools, list)
    assert "health_check" in tools
    assert "echo" in tools
    assert "server_info" in tools


@pytest.mark.asyncio
async def test_server_info_response_schema(server):
    result = await server.call_tool("server_info", {})
    data = result.structured_content
    assert isinstance(data, dict)
    assert "service" in data
    assert "version" in data
    assert "description" in data
    assert "tools" in data


@pytest.mark.asyncio
async def test_server_info_no_error(server):
    result = await server.call_tool("server_info", {})
    assert result.is_error is False


@pytest.mark.asyncio
async def test_server_info_description_is_concise(server):
    result = await server.call_tool("server_info", {})
    desc = result.structured_content["description"]
    assert len(desc) < 120


@pytest.mark.asyncio
async def test_server_info_description_mentions_capabilities(server):
    result = await server.call_tool("server_info", {})
    desc = result.structured_content["description"].lower()
    assert "health" in desc
    assert "echo" in desc


@pytest.mark.asyncio
async def test_server_info_includes_all_tools(server):
    result = await server.call_tool("server_info", {})
    tools = result.structured_content["tools"]
    assert "health_check" in tools
    assert "echo" in tools
    assert "server_info" in tools
    assert "create_task" in tools
    assert "list_tasks" in tools
    assert "update_task" in tools
    assert "delete_task" in tools


@pytest.mark.asyncio
async def test_server_info_tools_sorted(server):
    result = await server.call_tool("server_info", {})
    tools = result.structured_content["tools"]
    assert tools == sorted(tools)


@pytest.mark.asyncio
async def test_server_info_description_not_empty_str(server):
    result = await server.call_tool("server_info", {})
    desc = result.structured_content["description"]
    assert desc.strip() == desc
