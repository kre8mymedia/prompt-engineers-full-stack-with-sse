"""Returns Instance of ChatGPT Clone"""

from langchain import LLMChain
from langchain.memory import ConversationBufferWindowMemory
## Modules
from src.llms import LLM
from src.prompts.chat import CHAT_GPT_PROMPT

class ChatGptChain:  # pylint: disable=too-few-public-methods
    """Returns Instance of ChatGPT Clone"""
    def __init__(self, _token):
        self.token = _token

    def retrieve(
        self,
        temperature: float = 0,
        verbose: bool = False,
        memory_k: int = 2,
    ):
        chain = LLMChain(
            llm=LLM(self.token).model_select(temperature=temperature),
            prompt=CHAT_GPT_PROMPT,
            verbose=verbose,
            memory=ConversationBufferWindowMemory(k=memory_k),
        )
        return chain
