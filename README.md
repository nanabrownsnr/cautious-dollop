# cautious-dollop

A production-quality MCP (Model Context Protocol) server providing health checks, message echoing, and server information tools.

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
  "description": "A production-quality MCP server providing health checks, message echoing, and server information tools.",
  "tools": ["echo", "health_check", "server_info"]
}
```

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

## Development

### Running Tests

```bash
uv run pytest
```

### Linting

```bash
uv run ruff check .
```
