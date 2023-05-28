"""Status Models"""
from typing import Tuple, List
from pydantic import BaseModel, Field

class PostChatReqBody(BaseModel): # pylint: disable=too-few-public-methods
    """ReqBody for Post Chat Message"""
    question: str = Field(...)
    messages: List[str] = Field(...)

    class Config: # pylint: disable=too-few-public-methods
        """Example Config"""
        schema_extra = {
            "example": {
                "question": "Who were the pitchers?",
                "messages": [
                    'Who won the 2001 world series?',
                    'The 2001 World Series was won by the Arizona Diamondbacks. They defeated the New York Yankees in seven games to win their first championship in franchise history.'
                ]
            }
        }

class GetChatResponse(BaseModel): # pylint: disable=too-few-public-methods
    """Response for Post Chat Message"""
    class Config: # pylint: disable=too-few-public-methods
        """Example Get Chat Response"""
        schema_extra = {
            "example": {"answer": "The Arizona Diamondbacks had a strong pitching staff that included Randy Johnson and Curt Schilling, who were both named co-MVPs of the World Series. The New York Yankees had a solid pitching staff as well, with Roger Clemens, Andy Pettitte, and Mariano Rivera among their key pitchers."}
        }
        