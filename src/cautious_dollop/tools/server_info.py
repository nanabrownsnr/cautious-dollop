"""Server info MCP tool."""

from fastmcp import FastMCP

from cautious_dollop import __version__

SERVICE_NAME = "cautious-dollop"
SERVICE_DESCRIPTION = (
    "A production-quality MCP server providing health checks, "
    "message echoing, and server information tools."
)


def register_server_info(server: FastMCP) -> None:
    """Register the server_info tool on the given server."""

    @server.tool()
    async def server_info() -> dict:
        """Return information about this MCP server.

        Returns structured JSON with service name, version, description,
        and a list of registered tool names.
        """
        tools = await server.list_tools()
        tool_names = sorted(t.name for t in tools)
        return {
            "service": SERVICE_NAME,
            "version": __version__,
            "description": SERVICE_DESCRIPTION,
            "tools": tool_names,
        }
