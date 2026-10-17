# cautious-dollop

A production-quality MCP (Model Context Protocol) server providing health checks, message echoing, server information, and task management tools.

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

## Installation

```bash
uv sync
```

This installs all runtime and development dependencies.

## Running Locally

```bash
# Start the server (defaults to port 8000)
uv run python -m cautious_dollop

# Or with a custom port
PORT=9000 uv run python -m cautious_dollop
```

## Docker Execution

```bash
# Build and run with docker-compose
docker compose up

# Or build and run directly
docker build -t cautious-dollop .
docker run -p 8000:8000 cautious-dollop
```

## MCP Endpoint

The MCP server is exposed over HTTP at:

```
http://localhost:8000/mcp
```

## HTTP Health Endpoint

A GET endpoint is available for container health checks:

```
GET http://localhost:8000/health
```

Response:
```json
{
  "status": "ok",
  "service": "cautious-dollop",
  "version": "0.1.0"
}
```

## Available Tools

### health_check

Returns the health status of the service.

**Parameters:** None

**Response:**
```json
{
  "status": "ok",
  "service": "cautious-dollop",
  "version": "0.1.0"
}
```

### echo

Echoes back the provided message in structured JSON.

**Parameters:**
- `message` (string, required): The message to echo back.

**Response:**
```json
{
  "message": "Hello, world!"
}
```

### server_info

Returns information about this MCP server.

**Parameters:** None

**Response:**
```json
{
  "service": "cautious-dollop",
  "version": "0.1.0",
  "description": "A production-quality MCP server providing health checks, message echoing, server information, and task management tools.",
  "tools": ["create_task", "delete_task", "echo", "health_check", "list_tasks", "server_info", "update_task"]
}
```

### create_task

Creates a new task with the given title, optional description, and priority.

**Parameters:**
- `title` (string, required): The title of the task.
- `description` (string, optional): A description of the task.
- `priority` (string, optional): Task priority - `"low"`, `"medium"`, or `"high"`. Defaults to `"medium"`.

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Implement feature X",
  "description": "Add support for task management",
  "priority": "high",
  "status": "todo",
  "created_at": "2026-10-17T12:00:00+00:00"
}
```

**Validation:** Returns an error if the title is empty or the priority is invalid.

### list_tasks

Lists all tasks with optional filtering by status and priority.

**Parameters:**
- `status` (string, optional): Filter by status - `"todo"`, `"in_progress"`, or `"done"`.
- `priority` (string, optional): Filter by priority - `"low"`, `"medium"`, or `"high"`.

**Response:**
```json
{
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Implement feature X",
      "description": "Add support for task management",
      "priority": "high",
      "status": "todo",
      "created_at": "2026-10-17T12:00:00+00:00"
    }
  ],
  "count": 1
}
```

### update_task

Updates an existing task by ID. At least one field must be provided.

**Parameters:**
- `id` (string, required): The task ID to update.
- `title` (string, optional): New title.
- `description` (string, optional): New description.
- `priority` (string, optional): New priority - `"low"`, `"medium"`, or `"high"`.
- `status` (string, optional): New status - `"todo"`, `"in_progress"`, or `"done"`.

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated title",
  "description": "Updated description",
  "priority": "high",
  "status": "in_progress",
  "created_at": "2026-10-17T12:00:00+00:00"
}
```

**Validation:** Returns a 404 error if the task does not exist. Returns an error for invalid status or priority values.

### delete_task

Deletes a task by ID.

**Parameters:**
- `id` (string, required): The task ID to delete.

**Response:**
```json
{
  "deleted": true,
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Task '550e8400-e29b-41d4-a716-446655440000' has been successfully deleted."
}
```

**Validation:** Returns a 404 error if the task does not exist.

## Example Tool Calls

### Health Check

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "health_check",
    "arguments": {}
  }
}
```

### Echo

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "echo",
    "arguments": {
      "message": "Hello from MCP!"
    }
  }
}
```

### Server Info

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "server_info",
    "arguments": {}
  }
}
```

### Create Task

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "create_task",
    "arguments": {
      "title": "Implement feature X",
      "description": "Add support for task management",
      "priority": "high"
    }
  }
}
```

### List Tasks

```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "tools/call",
  "params": {
    "name": "list_tasks",
    "arguments": {
      "status": "todo",
      "priority": "high"
    }
  }
}
```

### Update Task

```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "method": "tools/call",
  "params": {
    "name": "update_task",
    "arguments": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "in_progress",
      "title": "Updated title"
    }
  }
}
```

### Delete Task

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "tools/call",
  "params": {
    "name": "delete_task",
    "arguments": {
      "id": "550e8400-e29b-41d4-a716-446655440000"
    }
  }
}
```

## Development

### Running Tests

```bash
uv run pytest
```

### Linting

```bash
uv run ruff check .
```
