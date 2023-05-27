"""Application entrypoint"""
import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
## Modules
from src.config import APP_ENV
from src.middleware.streaming import ConnectionMiddleware
## Routes
from src.routes.chat import router as chat_routes

app = FastAPI(
    title='Test Chat',
    version='v0.0.1'
)

# Enable CORS to allow requests from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(ConnectionMiddleware)

## Routing
app.include_router(chat_routes, prefix="/api/v1")

@app.get("/")
def read_root():
    """Root route"""
    return HTMLResponse(APP_ENV)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    