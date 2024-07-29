from operator import itemgetter
import os
import logging

from data_store import *

from .prompts import GENERATE_ANSWER_PROMPT, MULTI_QUERY_PROMPT
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain.load import dumps, loads

class QueryResolver:
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
            
    def answer_question(self, question: str, ds: VideoSearchDataStore) -> str:
        retriever = ds.get_retriever()

        generate_multi_queries = (
            ChatPromptTemplate.from_template(MULTI_QUERY_PROMPT)
            | self.__llm
            | StrOutputParser()
            | (lambda x: x.split("\n"))
            | (lambda lines: list(filter(lambda x: x != "", lines))) # To filter out any empty lines
        )

        print("\n\n\nMulti queries")
        print(generate_multi_queries.invoke({"question": question}))

        retrieval_chain = (
            generate_multi_queries
            | retriever.map()
            | self.get_unique_union
            | (lambda docs: [doc.page_content for doc in docs])
        )

        print("\n\n\nRetrieval chain")
        print(retrieval_chain.invoke({"question": question}))

        rag_chain = (
            {"context": retrieval_chain, "question": itemgetter("question")}
            | ChatPromptTemplate.from_template(GENERATE_ANSWER_PROMPT)
            | self.__llm
            | StrOutputParser()
        )

        logging.info(f"[LLM] Executing prompt: {rag_chain}")
        output = rag_chain.invoke({"question": question})

        return output
    
    def get_unique_union(self, documents: list[list]):
        """ Unique union of retrieved docs """
        # Flatten list of lists, and convert each Document to string
        flattened_docs = [dumps(doc) for sublist in documents for doc in sublist]
        # Get unique documents
        unique_docs = list(set(flattened_docs))
        # Return
        return [loads(doc) for doc in unique_docs]



