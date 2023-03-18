import asyncio
import os
import uuid
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Connection storage
connections = {}

# Enable CORS to allow requests from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ConnectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.connections = connections
        response = await call_next(request)
        return response


app.add_middleware(ConnectionMiddleware)

@app.get("/")
def read_root(request: Request):
    return HTMLResponse("Simple Event Source")


async def stream_generator(request: Request):
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


@app.get("/stream")
async def stream(request: Request):
    return StreamingResponse(stream_generator(request), media_type="text/event-stream")

@app.post("/message")
async def post_message(request: Request):
    data = await request.json()
    message = data.get("message", "")

    for queue in request.state.connections.values():
        await queue.put(message)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))