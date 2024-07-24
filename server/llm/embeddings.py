
import os
import logging

def get_embedding_func():
    use_openai = os.getenv("USE_OPENAI") == "1"
    if use_openai:
        logging.info("[LLM::Embeddings] Using OpenAI embeddings")

        EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY")

        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(api_key=EMBEDDING_API_KEY, model="text-embedding-3-small")
    else:
        logging.info("[LLM::Embeddings] Using Ollama embeddings")
        from langchain_community.embeddings.ollama import OllamaEmbeddings
        return OllamaEmbeddings(model='llama3.1:latest')  
