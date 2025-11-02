from httpx import AsyncClient
from mcp_bridge.config import config
from fastapi import Request
from contextlib import asynccontextmanager

async def create_client(request: Request = None):
    """Creates a new client instance with the appropriate headers"""
    
    # Extract API key from request header if enabled and provided, fallback to config
    auth_header = f"Bearer {config.inference_server.api_key}"
    
    if config.inference_server.use_client_key and request:
        # Check if authorization header exists (case-insensitive)
        headers_lower_map = {k.lower(): k for k in request.headers.keys()}
        if "authorization" in headers_lower_map:
            # Get the actual header name (preserving original case) and then its value
            actual_header_name = headers_lower_map["authorization"]
            auth_header = request.headers.get(actual_header_name)
    
    client = AsyncClient(
        base_url=config.inference_server.base_url,
        headers={
            "Authorization": auth_header,
            "Content-Type": "application/json"
        },
        timeout=10000,
    )
    
    if request:
        # Add headers from request
        headers = {k.lower(): v for k, v in request.headers.items()}
        
        openwebui_headers = [
            "x-openwebui-user-name",
            "x-openwebui-user-id",
            "x-openwebui-user-email",
            "x-openwebui-user-role"
        ]
        
        for header in openwebui_headers:
            if header in headers:
                client.headers[header] = headers[header]
    
    return client

@asynccontextmanager
async def get_client(request: Request = None):
    """Context manager for HTTP client"""
    client = await create_client(request)
    try:
        yield client
    finally:
        await client.aclose()
