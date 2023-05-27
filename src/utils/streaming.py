"""Utils for streaming support"""
import uuid
import asyncio
from fastapi import Request

async def stream_generator(request: Request):
    """Handles stream messages to client"""
    connection_id = str(uuid.uuid4())
    request.state.connections[connection_id] = asyncio.Queue()

    try:
        while True:
            data = await request.state.connections[connection_id].get()
            yield f"data: {data}\n\n"
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        del request.state.connections[connection_id]
        raise
    