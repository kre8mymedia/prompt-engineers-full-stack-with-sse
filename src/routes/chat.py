"""Chat Routes"""
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

## Modules
from src.chains.chat_gpt_chain import ChatGptChain
from src.utils import count_tokens
from src.config import APP_ENV, OPENAI_API_KEY
from src.utils.logging import logger
from src.utils.streaming import stream_generator

# prompt = PromptTemplate(
#     input_variables=["history", "human_input"],
#     template=CHAT_GPT_TEMPLATE
# )

# chatgpt_chain = LLMChain(
#     llm=LLM(OPENAI_API_KEY).model_select(),
#     prompt=prompt,
#     verbose=True,
#     memory=ConversationBufferWindowMemory(k=2),
# )

router = APIRouter()

@router.get("/stream")
async def stream(request: Request):
    return StreamingResponse(stream_generator(request), media_type="text/event-stream")

@router.post("/message")
async def post_message(request: Request):
    data = await request.json()
    message = data.get("message", "")
    chain = ChatGptChain(OPENAI_API_KEY).retrieve(verbose=APP_ENV == 'development')
    result = count_tokens(chain, message)
    logger.info(result)
    for queue in request.state.connections.values():
        await queue.put(message)
        await queue.put(result.get("result", ""))
        