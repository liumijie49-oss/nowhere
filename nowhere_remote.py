"""Minimal authenticated remote HTTP entry point for the Nowhere MCP server.

This does not change the original Nowhere game, tools, or its stdio entry point.
Railway variables required: NOWHERE_ACCESS_TOKEN (>= 40 chars), NOWHERE_HOME=/data.
Mount a persistent Railway Volume at /data before deploying.
"""

import os
import re

import uvicorn

from nowhere.server import mcp


def make_app():
    token = os.environ.get("NOWHERE_ACCESS_TOKEN", "").strip()
    if len(token) < 40 or re.fullmatch(r"[A-Za-z0-9_-]+", token) is None:
        raise RuntimeError(
            "Set NOWHERE_ACCESS_TOKEN to a random 40+ character URL-safe token "
            "in Railway Variables (never in GitHub)."
        )

    # Requests to /mcp and other routes do not expose the MCP tools.
    # The path itself is a sensitive credential. Keep it private.
    return mcp.http_app(path=f"/mcp/{token}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    uvicorn.run(make_app(), host="0.0.0.0", port=port, log_level="warning", access_log=False)
