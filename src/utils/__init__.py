"""Main Utils"""

import os
from langchain.callbacks import get_openai_callback
from langchain.text_splitter import (
    CharacterTextSplitter, 
    RecursiveCharacterTextSplitter)

########################################################
## History
########################################################
def get_chat_history(inputs: tuple):
    res = []
    for human, bot in inputs:
        res.append(f"Human:{human}\nAI:{bot}")
    return "\n".join(res)

########################################################
## Loaders
########################################################
def list_files(directory):
    files = os.listdir(directory)
    return files


########################################################
## Tokens
########################################################
def count_tokens(chain, query):
    with get_openai_callback() as callback:
        result = chain.predict(human_input=query)
        return {
            'result': result,
            'total_tokens': callback.total_tokens,
            'prompt_tokens': callback.prompt_tokens,
            'completion_tokens': callback.completion_tokens,
            'total_cost': callback.total_cost,
        }

########################################################
## Tokens
########################################################
def split_docs(
    documents,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    recursive: bool = False,
):
    ## Text Spliter
    if recursive:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )
    else:
        text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )
    docs = text_splitter.split_documents(documents)
    return docs
