"""Returns Instance of ChatGPT Clone"""
from langchain.memory import ConversationBufferWindowMemory
from langchain import LLMChain, PromptTemplate
## Modules
from src.llms import LLM

## Modules
from src.prompts.chat import CHAT_GPT_TEMPLATE

class ChatGptChain:  # pylint: disable=too-few-public-methods
    """Returns Instance of ChatGPT Clone"""
    def __init__(self, _token):
        self.token = _token

    def retrieve(
        self,
        temperature: float = 0,
        verbose: bool = False
    ):
        prompt = PromptTemplate(
            input_variables=["history", "human_input"],
            template=CHAT_GPT_TEMPLATE
        )
        chain = LLMChain(
            llm=LLM(self.token).model_select(temperature=temperature),
            prompt=prompt,
            verbose=verbose,
            memory=ConversationBufferWindowMemory(k=2),
        )
        return chain
