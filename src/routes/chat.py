"""Chat Routes"""
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

## Modules
from src.config import OPENAI_API_KEY
from src.utils.streaming import stream_generator

template = """Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

{history}
Human: {human_input}
Assistant:"""

prompt = PromptTemplate(
    input_variables=["history", "human_input"],
    template=template
)

chatgpt_chain = LLMChain(
    llm=OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY),
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
    result = chatgpt_chain.predict(human_input=message)
    print(result)
    for queue in request.state.connections.values():
        await queue.put(result)
        