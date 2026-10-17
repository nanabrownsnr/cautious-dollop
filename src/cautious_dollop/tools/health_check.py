"""Health check MCP tool."""

from fastmcp import FastMCP

from cautious_dollop import __version__

SERVICE_NAME = "cautious-dollop"


def register_health_check(server: FastMCP) -> None:
    """Register the health_check tool on the given server."""

    @server.tool()
    def health_check() -> dict:
        """Return the health status of the service.

        Returns structured JSON with status, service name, and version.
        """
        return {
            "status": "ok",
            "service": SERVICE_NAME,
            "version": __version__,
        }
