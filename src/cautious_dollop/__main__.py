"""Entry point for running the MCP server."""

import os

import uvicorn

from cautious_dollop.app import build_app


def main() -> None:
    """Start the MCP server."""
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", "8000"))

    app = build_app()

    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        log_level="info",
        timeout_graceful_shutdown=0,
        lifespan="on",
    )
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    main()
