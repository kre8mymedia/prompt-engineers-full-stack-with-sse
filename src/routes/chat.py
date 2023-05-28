"""Chat Routes"""
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

## Modules
from src.llms import LLM
from src.prompts.chat import CHAT_GPT_TEMPLATE
from src.utils import count_tokens
from src.config import OPENAI_API_KEY
from src.utils.logging import logger
from src.utils.streaming import stream_generator

prompt = PromptTemplate(
    input_variables=["history", "human_input"],
    template=CHAT_GPT_TEMPLATE
)

chatgpt_chain = LLMChain(
    llm=LLM(OPENAI_API_KEY).model_select(),
    prompt=prompt,
    verbose=True,
    memory=ConversationBufferWindowMemory(k=2),
)

router = APIRouter()

@router.get("/stream")
async def stream(request: Request):
    return StreamingResponse(stream_generator(request), media_type="text/event-stream")

@router.post("/message")
async def post_message(request: Request):
    data = await request.json()
    message = data.get("message", "")
    result = count_tokens(chatgpt_chain, message)
    logger.info(result)
    for queue in request.state.connections.values():
        await queue.put(message)
        await queue.put(result.get("result", ""))
        