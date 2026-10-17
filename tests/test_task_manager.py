"""Tests for task management MCP tools."""

import asyncio

import pytest

from cautious_dollop.server import create_server
from cautious_dollop.tools.task_manager import (
    _store,
)


@pytest.fixture
def server():
    """Return a fresh server instance with a clean task store."""
    _store.clear()
    yield create_server()
    _store.clear()


# ===================== create_task tests =====================


class TestCreateTask:
    @pytest.mark.asyncio
    async def test_create_task_minimal(self, server):
        result = await server.call_tool("create_task", {"title": "My Task"})
        assert result.is_error is False
        data = result.structured_content
        assert data["title"] == "My Task"
        assert data["status"] == "todo"
        assert data["priority"] == "medium"
        assert data["description"] == ""
        assert data["id"] is not None
        assert data["created_at"] is not None

    @pytest.mark.asyncio
    async def test_create_task_full(self, server):
        result = await server.call_tool("create_task", {
            "title": "Full Task",
            "description": "A complete task",
            "priority": "high",
        })
        assert result.is_error is False
        data = result.structured_content
        assert data["title"] == "Full Task"
        assert data["description"] == "A complete task"
        assert data["priority"] == "high"
        assert data["status"] == "todo"

    @pytest.mark.asyncio
    async def test_create_task_low_priority(self, server):
        result = await server.call_tool("create_task", {
            "title": "Low Priority",
            "priority": "low",
        })
        assert result.is_error is False
        assert result.structured_content["priority"] == "low"

    @pytest.mark.asyncio
    async def test_create_task_medium_priority(self, server):
        result = await server.call_tool("create_task", {
            "title": "Medium Priority",
            "priority": "medium",
        })
        assert result.is_error is False
        assert result.structured_content["priority"] == "medium"

    @pytest.mark.asyncio
    async def test_create_task_high_priority(self, server):
        result = await server.call_tool("create_task", {
            "title": "High Priority",
            "priority": "high",
        })
        assert result.is_error is False
        assert result.structured_content["priority"] == "high"

    @pytest.mark.asyncio
    async def test_create_task_default_priority(self, server):
        result = await server.call_tool("create_task", {"title": "Default Priority"})
        assert result.is_error is False
        assert result.structured_content["priority"] == "medium"

    @pytest.mark.asyncio
    async def test_create_task_unique_ids(self, server):
        result1 = await server.call_tool("create_task", {"title": "Task 1"})
        result2 = await server.call_tool("create_task", {"title": "Task 2"})
        assert result1.structured_content["id"] != result2.structured_content["id"]

    @pytest.mark.asyncio
    async def test_create_task_response_schema(self, server):
        result = await server.call_tool("create_task", {"title": "Schema Test"})
        data = result.structured_content
        assert isinstance(data, dict)
        assert "id" in data
        assert "title" in data
        assert "description" in data
        assert "priority" in data
        assert "status" in data
        assert "created_at" in data
        assert len(data) == 6

    @pytest.mark.asyncio
    async def test_create_task_empty_title_returns_error(self, server):
        result = await server.call_tool("create_task", {"title": ""})
        assert result.structured_content["error"] is True
        assert result.structured_content["error"] is True
        assert "Title is required" in result.structured_content["message"]

    @pytest.mark.asyncio
    async def test_create_task_whitespace_title_returns_error(self, server):
        result = await server.call_tool("create_task", {"title": "   "})
        assert result.structured_content["error"] is True
        assert result.structured_content["error"] is True

    @pytest.mark.asyncio
    async def test_create_task_invalid_priority_returns_error(self, server):
        result = await server.call_tool("create_task", {
            "title": "Bad Priority",
            "priority": "critical",
        })
        assert result.structured_content["error"] is True
        assert result.structured_content["error"] is True
        assert "Invalid priority" in result.structured_content["message"]

    @pytest.mark.asyncio
    async def test_create_task_stores_task(self, server):
        await server.call_tool("create_task", {"title": "Stored Task"})
        list_result = await server.call_tool("list_tasks", {})
        assert list_result.structured_content["count"] == 1
        assert list_result.structured_content["tasks"][0]["title"] == "Stored Task"


# ===================== list_tasks tests =====================


class TestListTasks:
    @pytest.mark.asyncio
    async def test_list_tasks_empty(self, server):
        result = await server.call_tool("list_tasks", {})
        assert result.is_error is False
        assert result.structured_content["count"] == 0
        assert result.structured_content["tasks"] == []

    @pytest.mark.asyncio
    async def test_list_tasks_returns_all(self, server):
        await server.call_tool("create_task", {"title": "Task 1"})
        await server.call_tool("create_task", {"title": "Task 2"})
        result = await server.call_tool("list_tasks", {})
        assert result.structured_content["count"] == 2

    @pytest.mark.asyncio
    async def test_list_tasks_filter_by_status(self, server):
        await server.call_tool("create_task", {"title": "Todo Task"})
        created = await server.call_tool("create_task", {"title": "High Task", "priority": "high"})
        task_id = created.structured_content["id"]
        await server.call_tool("update_task", {"id": task_id, "status": "in_progress"})

        result = await server.call_tool("list_tasks", {"status": "todo"})
        assert result.structured_content["count"] == 1
        assert result.structured_content["tasks"][0]["title"] == "Todo Task"

    @pytest.mark.asyncio
    async def test_list_tasks_filter_by_priority(self, server):
        await server.call_tool("create_task", {"title": "Low Task", "priority": "low"})
        await server.call_tool("create_task", {"title": "High Task", "priority": "high"})

        result = await server.call_tool("list_tasks", {"priority": "low"})
        assert result.structured_content["count"] == 1
        assert result.structured_content["tasks"][0]["title"] == "Low Task"

    @pytest.mark.asyncio
    async def test_list_tasks_filter_by_both(self, server):
        await server.call_tool("create_task", {"title": "Todo Low", "priority": "low"})
        created = await server.call_tool("create_task", {"title": "Done Low", "priority": "low"})
        done_task_id = created.structured_content["id"]
        await server.call_tool("update_task", {"id": done_task_id, "status": "done"})

        result = await server.call_tool("list_tasks", {"status": "todo", "priority": "low"})
        assert result.structured_content["count"] == 1
        assert result.structured_content["tasks"][0]["title"] == "Todo Low"

    @pytest.mark.asyncio
    async def test_list_tasks_invalid_status_filter(self, server):
        result = await server.call_tool("list_tasks", {"status": "invalid"})
        assert result.structured_content["error"] is True
        assert result.structured_content["error"] is True
        assert "Invalid status filter" in result.structured_content["message"]

    @pytest.mark.asyncio
    async def test_list_tasks_invalid_priority_filter(self, server):
        result = await server.call_tool("list_tasks", {"priority": "critical"})
        assert result.structured_content["error"] is True
        assert result.structured_content["error"] is True
        assert "Invalid priority filter" in result.structured_content["message"]

    @pytest.mark.asyncio
    async def test_list_tasks_response_schema(self, server):
        result = await server.call_tool("list_tasks", {})
        data = result.structured_content
        assert isinstance(data, dict)
        assert "tasks" in data
        assert "count" in data
        assert isinstance(data["tasks"], list)
        assert isinstance(data["count"], int)

    @pytest.mark.asyncio
    async def test_list_tasks_task_structure(self, server):
        await server.call_tool("create_task", {"title": "Structure Test"})
        result = await server.call_tool("list_tasks", {})
        task = result.structured_content["tasks"][0]
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "priority" in task
        assert "status" in task
        assert "created_at" in task


# ===================== update_task tests =====================


class TestUpdateTask:
    @pytest.mark.asyncio
    async def test_update_task_title(self, server):
        created = await server.call_tool("create_task", {"title": "Old Title"})
        task_id = created.structured_content["id"]
        result = await server.call_tool("update_task", {"id": task_id, "title": "New Title"})
        assert result.is_error is False
        assert result.structured_content["title"] == "New Title"

    @pytest.mark.asyncio
    async def test_update_task_description(self, server):
        created = await server.call_tool("create_task", {"title": "Task"})
        task_id = created.structured_content["id"]
        result = await server.call_tool("update_task", {"id": task_id, "description": "New desc"})
        assert result.is_error is False
        assert result.structured_content["description"] == "New desc"

    @pytest.mark.asyncio
    async def test_update_task_priority(self, server):
        created = await server.call_tool("create_task", {"title": "Task", "priority": "low"})
        task_id = created.structured_content["id"]
        result = await server.call_tool("update_task", {"id": task_id, "priority": "high"})
        assert result.is_error is False
        assert result.structured_content["priority"] == "high"

    @pytest.mark.asyncio
    async def test_update_task_status(self, server):
        created = await server.call_tool("create_task", {"title": "Task"})
        task_id = created.structured_content["id"]
        result = await server.call_tool("update_task", {"id": task_id, "status": "in_progress"})
        assert result.is_error is False
        assert result.structured_content["status"] == "in_progress"

    @pytest.mark.asyncio
    async def test_update_task_multiple_fields(self, server):
        created = await server.call_tool("create_task", {
            "title": "Original",
            "description": "Original desc",
        })
        task_id = created.structured_content["id"]
        result = await server.call_tool("update_task", {
            "id": task_id,
            "title": "Updated",
            "status": "done",
            "priority": "high",
        })
        assert result.is_error is False
        assert result.structured_content["title"] == "Updated"
        assert result.structured_content["status"] == "done"
        assert result.structured_content["priority"] == "high"

    @pytest.mark.asyncio
    async def test_update_task_preserves_other_fields(self, server):
        created = await server.call_tool("create_task", {"title": "Original"})
        task_id = created.structured_content["id"]
        created_at = created.structured_content["created_at"]
        result = await server.call_tool("update_task", {"id": task_id, "title": "New"})
        assert result.structured_content["id"] == task_id
        assert result.structured_content["created_at"] == created_at

    @pytest.mark.asyncio
    async def test_update_task_not_found(self, server):
        result = await server.call_tool("update_task", {
            "id": "nonexistent-id",
            "title": "New Title",
        })
        assert result.structured_content["error"] is True
        assert result.structured_content["error"] is True
        assert "Task not found" in result.structured_content["message"]
        assert result.structured_content["code"] == 404

    @pytest.mark.asyncio
    async def test_update_task_empty_id(self, server):
        result = await server.call_tool("update_task", {"id": ""})
        assert result.structured_content["error"] is True
        assert result.structured_content["error"] is True

    @pytest.mark.asyncio
    async def test_update_task_invalid_status(self, server):
        created = await server.call_tool("create_task", {"title": "Task"})
        task_id = created.structured_content["id"]
        result = await server.call_tool("update_task", {"id": task_id, "status": "cancelled"})
        assert result.structured_content["error"] is True
        assert result.structured_content["error"] is True
        assert "Invalid status" in result.structured_content["message"]

    @pytest.mark.asyncio
    async def test_update_task_invalid_priority(self, server):
        created = await server.call_tool("create_task", {"title": "Task"})
        task_id = created.structured_content["id"]
        result = await server.call_tool("update_task", {"id": task_id, "priority": "urgent"})
        assert result.structured_content["error"] is True
        assert result.structured_content["error"] is True
        assert "Invalid priority" in result.structured_content["message"]

    @pytest.mark.asyncio
    async def test_update_task_no_fields_provided(self, server):
        created = await server.call_tool("create_task", {"title": "Task"})
        task_id = created.structured_content["id"]
        result = await server.call_tool("update_task", {"id": task_id})
        assert result.structured_content["error"] is True
        assert result.structured_content["error"] is True
        assert "At least one field" in result.structured_content["message"]

    @pytest.mark.asyncio
    async def test_update_task_all_statuses(self, server):
        for status in ["todo", "in_progress", "done"]:
            created = await server.call_tool("create_task", {"title": "Task"})
            task_id = created.structured_content["id"]
            result = await server.call_tool("update_task", {"id": task_id, "status": status})
            assert result.is_error is False
            assert result.structured_content["status"] == status

    @pytest.mark.asyncio
    async def test_update_task_response_schema(self, server):
        created = await server.call_tool("create_task", {"title": "Schema Test"})
        task_id = created.structured_content["id"]
        result = await server.call_tool("update_task", {"id": task_id, "title": "Updated"})
        data = result.structured_content
        assert isinstance(data, dict)
        assert "id" in data
        assert "title" in data
        assert "description" in data
        assert "priority" in data
        assert "status" in data
        assert "created_at" in data


# ===================== delete_task tests =====================


class TestDeleteTask:
    @pytest.mark.asyncio
    async def test_delete_task_success(self, server):
        created = await server.call_tool("create_task", {"title": "To Delete"})
        task_id = created.structured_content["id"]
        result = await server.call_tool("delete_task", {"id": task_id})
        assert result.is_error is False
        assert result.structured_content["deleted"] is True
        assert result.structured_content["id"] == task_id

    @pytest.mark.asyncio
    async def test_delete_task_removes_from_list(self, server):
        created = await server.call_tool("create_task", {"title": "To Delete"})
        task_id = created.structured_content["id"]
        await server.call_tool("delete_task", {"id": task_id})
        list_result = await server.call_tool("list_tasks", {})
        assert list_result.structured_content["count"] == 0

    @pytest.mark.asyncio
    async def test_delete_task_confirmation_message(self, server):
        created = await server.call_tool("create_task", {"title": "Msg Test"})
        task_id = created.structured_content["id"]
        result = await server.call_tool("delete_task", {"id": task_id})
        assert "deleted" in result.structured_content["message"].lower()

    @pytest.mark.asyncio
    async def test_delete_task_not_found(self, server):
        result = await server.call_tool("delete_task", {"id": "nonexistent-id"})
        assert result.structured_content["error"] is True
        assert result.structured_content["error"] is True
        assert "Task not found" in result.structured_content["message"]
        assert result.structured_content["code"] == 404

    @pytest.mark.asyncio
    async def test_delete_task_empty_id(self, server):
        result = await server.call_tool("delete_task", {"id": ""})
        assert result.structured_content["error"] is True
        assert result.structured_content["error"] is True

    @pytest.mark.asyncio
    async def test_delete_task_response_schema(self, server):
        created = await server.call_tool("create_task", {"title": "Schema"})
        task_id = created.structured_content["id"]
        result = await server.call_tool("delete_task", {"id": task_id})
        data = result.structured_content
        assert isinstance(data, dict)
        assert "deleted" in data
        assert "id" in data
        assert "message" in data
        assert data["deleted"] is True

    @pytest.mark.asyncio
    async def test_delete_task_by_id_preserves_other_tasks(self, server):
        await server.call_tool("create_task", {"title": "Keep 1"})
        t2 = await server.call_tool("create_task", {"title": "Delete Me"})
        await server.call_tool("create_task", {"title": "Keep 2"})
        await server.call_tool("delete_task", {"id": t2.structured_content["id"]})
        list_result = await server.call_tool("list_tasks", {})
        assert list_result.structured_content["count"] == 2
        titles = [t["title"] for t in list_result.structured_content["tasks"]]
        assert "Keep 1" in titles
        assert "Keep 2" in titles
        assert "Delete Me" not in titles


# ===================== server integration tests =====================


class TestServerIntegration:
    @pytest.mark.asyncio
    async def test_server_has_all_task_tools(self, server):
        tools = await server.list_tools()
        tool_names = [t.name for t in tools]
        assert "create_task" in tool_names
        assert "list_tasks" in tool_names
        assert "update_task" in tool_names
        assert "delete_task" in tool_names

    def test_server_info_includes_task_tools(self, server):
        result = asyncio.run(server.call_tool("server_info", {}))
        tools = result.structured_content["tools"]
        assert "create_task" in tools
        assert "list_tasks" in tools
        assert "update_task" in tools
        assert "delete_task" in tools
