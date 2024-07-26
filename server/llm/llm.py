import os
import logging

from .prompts import GENERATE_ANSWER_PROMPT
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate

class LLM:
    def __init__(self) -> None:
        self.__use_openai = os.getenv("USE_OPENAI") == "1"

        if self.__use_openai:
            logging.info("[LLM::Embeddings] Using OpenAI models embeddings")

            from langchain_openai import OpenAIEmbeddings, ChatOpenAI
            OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
            self.__embedding_func = OpenAIEmbeddings(model="text-embedding-3-small", api_key=OPENAI_API_KEY)
            self.__llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)

        else:
            logging.info("[LLM::Embeddings] Using Ollama embeddings")

            from langchain_ollama import ChatOllama, OllamaEmbeddings
            self.__embedding_func = OllamaEmbeddings(model='llama3.1:latest')
            self.__llm = ChatOllama(model='llama3.1:latest', temperature=0)


    def get_embedding_func(self):
        return self.__embedding_func
            
    def answer_question(self, context: str, question: str) -> str:
        rag_chain = (
            {"context": lambda x: context, "question": RunnablePassthrough()}
            | ChatPromptTemplate.from_template(GENERATE_ANSWER_PROMPT)
            | self.__llm
            | StrOutputParser()
        )

        print(rag_chain.input_schema.schema())
        print(rag_chain.output_schema.schema())

        logging.info(f"[LLM] Executing prompt: {rag_chain}")
        output = rag_chain.invoke(question)

        return output



