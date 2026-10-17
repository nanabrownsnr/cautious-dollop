"""Task management MCP tools with in-memory storage."""

import uuid
from datetime import UTC, datetime
from enum import StrEnum

from fastmcp import FastMCP


class Priority(StrEnum):
    """Task priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(StrEnum):
    """Task status values."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


VALID_STATUSES = {"todo", "in_progress", "done"}
VALID_PRIORITIES = {"low", "medium", "high"}


class TaskStore:
    """In-memory task storage with thread-safe operations."""

    def __init__(self):
        self._tasks: dict[str, dict] = {}

    def create(self, title: str, description: str | None = None,
               priority: str = "medium") -> dict:
        task_id = str(uuid.uuid4())
        now = datetime.now(UTC).isoformat()
        task = {
            "id": task_id,
            "title": title,
            "description": description or "",
            "priority": priority,
            "status": "todo",
            "created_at": now,
        }
        self._tasks[task_id] = task
        return task

    def get(self, task_id: str) -> dict | None:
        return self._tasks.get(task_id)

    def list_all(self, status: str | None = None,
                 priority: str | None = None) -> list[dict]:
        tasks = list(self._tasks.values())
        if status:
            tasks = [t for t in tasks if t["status"] == status]
        if priority:
            tasks = [t for t in tasks if t["priority"] == priority]
        return tasks

    def update(self, task_id: str, **kwargs) -> dict | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        for key, value in kwargs.items():
            if key in task:
                task[key] = value
        return task

    def delete(self, task_id: str) -> bool:
        return self._tasks.pop(task_id, None) is not None

    def clear(self) -> None:
        self._tasks.clear()


_store = TaskStore()


def _error(message: str, code: int = 400) -> dict:
    return {
        "error": True,
        "message": message,
        "code": code,
    }


def register_task_manager(server: FastMCP) -> None:
    """Register task management tools on the given server."""

    @server.tool()
    def create_task(title: str, description: str | None = None,
                    priority: str | None = "medium") -> dict:
        """Create a new task.

        Args:
            title: The title of the task (required).
            description: Optional description of the task.
            priority: Task priority - 'low', 'medium', or 'high'
                (default: 'medium').

        Returns:
            Structured JSON containing the created task with id, title,
            description, priority, status, and created_at fields.

        Raises:
            ValidationError: If title is empty or priority is invalid.
        """
        if not title or not title.strip():
            return _error("Title is required and cannot be empty.")

        title = title.strip()

        if priority not in VALID_PRIORITIES:
            allowed = ", ".join(sorted(VALID_PRIORITIES))
            return _error(
                f"Invalid priority: '{priority}'. "
                f"Must be one of: {allowed}."
            )

        task = _store.create(title=title, description=description,
                             priority=priority)
        return {
            "id": task["id"],
            "title": task["title"],
            "description": task["description"],
            "priority": task["priority"],
            "status": task["status"],
            "created_at": task["created_at"],
        }

    @server.tool()
    def list_tasks(status: str | None = None,
                   priority: str | None = None) -> dict:
        """List all tasks with optional filtering.

        Args:
            status: Optional filter by status ('todo', 'in_progress', 'done').
            priority: Optional filter by priority ('low', 'medium', 'high').

        Returns:
            Structured JSON containing a list of tasks matching the filters.

        Raises:
            ValidationError: If status or priority filter values are invalid.
        """
        if status and status not in VALID_STATUSES:
            allowed = ", ".join(sorted(VALID_STATUSES))
            return _error(
                f"Invalid status filter: '{status}'. "
                f"Must be one of: {allowed}."
            )

        if priority and priority not in VALID_PRIORITIES:
            allowed = ", ".join(sorted(VALID_PRIORITIES))
            return _error(
                f"Invalid priority filter: '{priority}'. "
                f"Must be one of: {allowed}."
            )

        tasks = _store.list_all(status=status, priority=priority)
        return {
            "tasks": tasks,
            "count": len(tasks),
        }

    @server.tool()
    def update_task(id: str, title: str | None = None,
                    description: str | None = None,
                    priority: str | None = None,
                    status: str | None = None) -> dict:
        """Update an existing task.

        Args:
            id: The task ID to update (required).
            title: Optional new title.
            description: Optional new description.
            priority: Optional new priority ('low', 'medium', 'high').
            status: Optional new status ('todo', 'in_progress', 'done').

        Returns:
            Structured JSON containing the updated task.

        Raises:
            ValidationError: If task ID is missing/empty or update values
                are invalid.
        """
        if not id or not id.strip():
            return _error("Task ID is required and cannot be empty.")

        id = id.strip()

        if status and status not in VALID_STATUSES:
            allowed = ", ".join(sorted(VALID_STATUSES))
            return _error(
                f"Invalid status: '{status}'. "
                f"Must be one of: {allowed}."
            )

        if priority and priority not in VALID_PRIORITIES:
            allowed = ", ".join(sorted(VALID_PRIORITIES))
            return _error(
                f"Invalid priority: '{priority}'. "
                f"Must be one of: {allowed}."
            )

        if (not title and not description and
                priority is None and status is None):
            return _error(
                "At least one field (title, description, "
                "priority, or status) must be provided for update."
            )

        updated = _store.update(
            id, title=title, description=description,
            priority=priority, status=status
        )
        if updated is None:
            return _error(f"Task not found with ID: '{id}'.", code=404)

        return {
            "id": updated["id"],
            "title": updated["title"],
            "description": updated["description"],
            "priority": updated["priority"],
            "status": updated["status"],
            "created_at": updated["created_at"],
        }

    @server.tool()
    def delete_task(id: str) -> dict:
        """Delete a task.

        Args:
            id: The task ID to delete (required).

        Returns:
            Structured JSON confirmation of deletion.

        Raises:
            ValidationError: If task ID is missing/empty.
        """
        if not id or not id.strip():
            return _error("Task ID is required and cannot be empty.")

        id = id.strip()

        deleted = _store.delete(id)
        if not deleted:
            return _error(f"Task not found with ID: '{id}'.", code=404)

        return {
            "deleted": True,
            "id": id,
            "message": f"Task '{id}' has been successfully deleted.",
        }
