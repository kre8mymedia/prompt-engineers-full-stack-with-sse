"""Handles Streaming Middleware"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class ConnectionMiddleware(BaseHTTPMiddleware):
    """Handle streaming middleware"""
    def __init__(self, app, **options):
        super().__init__(app, **options)
        self.connections = {}

    async def dispatch(self, request: Request, call_next):
        request.state.connections = self.connections
        response = await call_next(request)
        return response
    