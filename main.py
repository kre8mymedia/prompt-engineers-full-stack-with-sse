"""Application entrypoint"""
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

## Modules
from src.utils.logging import logger
from src.models.status import StatusResponse
from src.config import APP_ENV, APP_VERSION, APP_NAME
from src.middleware.streaming import ConnectionMiddleware
## Routes
from src.routes.chat import router as chat_routes

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

#######################################################################
## Middleware
#######################################################################
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(ConnectionMiddleware)

#######################################################################
## Routes
#######################################################################
app.include_router(chat_routes, prefix="/api/v1")

#######################################################################
###  Check App Status
#######################################################################
@app.get("/status", tags=["Status"], response_model=StatusResponse)
async def get_application_version():
    try:
        if APP_VERSION:
            return {"version": APP_VERSION}
    except Exception as err:
        logger.exception(err)
        raise HTTPException(status_code=500, detail=str(err)) from err

#######################################################################
###  Pages
#######################################################################
@app.get("/", include_in_schema=False)
def read_root():
    """Root route"""
    return HTMLResponse(APP_ENV)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    