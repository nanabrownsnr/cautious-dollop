"""MCP server configuration with all tools registered."""

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from cautious_dollop import __version__
from cautious_dollop.tools.echo import register_echo
from cautious_dollop.tools.health_check import register_health_check
from cautious_dollop.tools.server_info import register_server_info
from cautious_dollop.tools.task_manager import register_task_manager

SERVER_NAME = "cautious-dollop"
SERVER_DESCRIPTION = (
    "A production-quality MCP server providing health checks, "
    "message echoing, server information, and task management tools."
)


async def _health_endpoint(request: Request) -> JSONResponse:
    """Health check HTTP endpoint handler."""
    return JSONResponse(
        content={
            "status": "ok",
            "service": SERVER_NAME,
            "version": __version__,
        }
    )


def create_server() -> FastMCP:
    """Create and configure the FastMCP server with all tools.

    Returns:
        A configured FastMCP server instance.
    """
    server = FastMCP(
        name=SERVER_NAME,
        instructions=SERVER_DESCRIPTION,
        version=__version__,
    )

    # Register health check tool
    register_health_check(server)

    # Register echo tool
    register_echo(server)

    # Register server info tool
    register_server_info(server)

    # Register task management tool
    register_task_manager(server)

    # Register HTTP health endpoint
    server.custom_route("/health", methods=["GET"])(_health_endpoint)

    return server
