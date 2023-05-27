"""Chat Routes"""
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
## Modules
from src.utils.streaming import stream_generator

router = APIRouter()

@router.get("/stream")
async def stream(request: Request):
    return StreamingResponse(stream_generator(request), media_type="text/event-stream")

@router.post("/message")
async def post_message(request: Request):
    data = await request.json()
    message = data.get("message", "")

    for queue in request.state.connections.values():
        await queue.put(message)
        