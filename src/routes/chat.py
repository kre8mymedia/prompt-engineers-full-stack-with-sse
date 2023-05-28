"""Chat Routes"""
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

## Modules
from src.config import APP_ENV, OPENAI_API_KEY
from src.chains.chat_gpt_chain import ChatGptChain
from src.config.swagger import CHAT_RESPONSE_DESCRIPTION, CHAT_ROUTE_DESCRIPTION
from src.models.chat import GetChatResponse, PostChatReqBody
from src.utils import count_tokens
from src.utils.logging import logger
from src.utils.streaming import stream_generator

router = APIRouter()

## Chains
chain = ChatGptChain(OPENAI_API_KEY).retrieve(verbose=APP_ENV == 'development')

@router.get(
    "/chat", 
    tags=["Chat"],
    response_model=GetChatResponse,
    responses={
        200: {
            "description": CHAT_RESPONSE_DESCRIPTION,
            "content": {"text/event-stream": {}}
        }
    },
    description=CHAT_ROUTE_DESCRIPTION,
)
async def get_chat_messages(request: Request):
    return StreamingResponse(stream_generator(request), media_type="text/event-stream")

@router.post("/chat", tags=["Chat"])
async def post_chat_message(request: Request, data: PostChatReqBody):
    data = await request.json()
    question = data.get("question", "")
    messages = data.get("messages", [])
    answer = count_tokens(chain, question)
    logger.info(messages)
    logger.info(answer)
    for queue in request.state.connections.values():
        await queue.put(question)
        await queue.put(answer.get("result", ""))
        