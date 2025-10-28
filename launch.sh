#!/bin/sh

# Load environment variables from .env and .secrets files if they exist
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi
if [ -f .secrets ]; then
    export $(grep -v '^#' .secrets | xargs)
fi

#echo $MCP_BRIDGE__INFERENCE_SERVER__API_KEY

# Start the MCP Bridge service
uv run mcp_bridge/main.py
#uvx git+https://github.com/secretiveshell/mcp-bridge.git
