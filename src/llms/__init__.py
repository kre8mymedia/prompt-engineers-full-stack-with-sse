"""Models Select"""
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class LLM: # pylint: disable=too-few-public-methods
    """LLM Service"""
    def __init__(self, _token):
        self.token = _token

    def model_select(
        self,
        model_name: str = 'gpt-3.5-turbo',
        temperature: float or int = 0,
        streaming: bool = False,
    ):
        if model_name in {'gpt-3.5-turbo', 'gpt-4'}:
            return ChatOpenAI(
                temperature=temperature,
                model_name=model_name,
                streaming=streaming,
                callbacks=[StreamingStdOutCallbackHandler()],
                openai_api_key=self.token
            )

        return OpenAI(
            temperature=temperature,
            model_name=model_name,
            streaming=streaming,
            openai_api_key=self.token
        )
    