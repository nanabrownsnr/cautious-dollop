"""Echo MCP tool."""

from fastmcp import FastMCP


def register_echo(server: FastMCP) -> None:
    """Register the echo tool on the given server."""

    @server.tool()
    def echo(message: str) -> dict:
        """Echo back the provided message.

        Args:
            message: The string message to echo back.

        Returns:
            Structured JSON containing the echoed message.
        """
        return {
            "message": message,
        }
