"""Application factory for the MCP server."""

from cautious_dollop.server import create_server


def build_app():
    """Build the Starlette application with MCP and /health endpoints.

    Returns:
        A Starlette application with MCP HTTP transport and health endpoint.
    """
    server = create_server()
    return server.http_app()
