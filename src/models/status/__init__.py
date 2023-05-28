"""Status Models"""
from pydantic import BaseModel, Field

from src.config import APP_VERSION

class StatusResponse(BaseModel): # pylint: disable=too-few-public-methods
    """Response for Status Endpoint"""
    version: str = Field(example=APP_VERSION)
    