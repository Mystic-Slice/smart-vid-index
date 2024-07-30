from operator import itemgetter
import os
import logging

from data_store import *

from .prompts import GENERATE_ANSWER_PROMPT, GENERATE_VIDEO_SUMMARY, MULTI_QUERY_PROMPT
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain.load import dumps, loads
from qdrant_client.http import models
class QueryResolver:
    def __init__(self) -> None:
        self.__use_openai = os.getenv("USE_OPENAI") == "1"

        if self.__use_openai:
            logging.info("[LLM] Using OpenAI models embeddings")

            from langchain_openai import OpenAIEmbeddings, ChatOpenAI
            OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
            self.__embedding_func = OpenAIEmbeddings(model="text-embedding-3-small", api_key=OPENAI_API_KEY)
            self.__llm = ChatOpenAI(
                model_name="gpt-4o-mini", 
                temperature=0, 
                api_key=OPENAI_API_KEY
            )

        else:
            logging.info("[LLM] Using Ollama embeddings")

            from langchain_ollama import ChatOllama, OllamaEmbeddings
            self.__embedding_func = OllamaEmbeddings(model='llama3.1:latest')
            self.__llm = ChatOllama(
                model='llama3.1:latest', 
                temperature=0, 
                base_url=os.getenv("OLLAMA_URL")
            )


    def get_embedding_func(self):
        return self.__embedding_func
    
    def get_relevant_videos(self, multi_queries: list[str], ds: VideoSearchDataStore) -> list[Document]:
        video_retriever = ds.get_video_retriever(search_kwargs={'k': 5})

        retrieval_chain = (
            video_retriever.map()
            | self.get_unique_union
        )

        output = retrieval_chain.invoke(multi_queries)
        return output
            
    def answer_question(self, question: str, ds: VideoSearchDataStore) -> str:
        multi_queries_chain = (
            ChatPromptTemplate.from_template(MULTI_QUERY_PROMPT)
            | self.__llm
            | StrOutputParser()
            | (lambda x: x.split("\n"))
            | (lambda lines: list(filter(lambda x: x != "", lines))) # To filter out any empty lines
        )

        logging.info(f"[LLM] Executing prompt to generate multi queries: {multi_queries_chain}")
        multi_queries = multi_queries_chain.invoke({"question": question})
        logging.info(f"[LLM] Generated multi queries: {multi_queries}")

        logging.info(f"[LLM] Retrieving relevant videos to generate context")
        relevant_videos = self.get_relevant_videos(multi_queries, ds)
        video_ids = [doc.metadata["video_id"] for doc in relevant_videos]
        logging.info("[LLM] Retrieved relevant videos: \n" + "\n".join([doc.metadata["title"] for doc in relevant_videos]))

        search_kwargs = {
            "k": 10,
            "filter": models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.video_id",
                        match=models.MatchAny(
                            any=video_ids
                        )
                    )
                ]
            )
        }
        caption_retriever = ds.get_caption_retriever(search_kwargs=search_kwargs)

        retrieval_chain = (
            caption_retriever.map()
            | self.get_unique_union
            | (lambda docs: [doc.page_content for doc in docs])
        )

        logging.info(f"[LLM] Retrieving relevant captions to generate context: {retrieval_chain}")
        relevant_captions = retrieval_chain.invoke(multi_queries)
        context = "\n".join(relevant_captions)
        logging.info(f"[LLM] Generated context: {context}")

        rag_chain = (
            {"context": itemgetter("context"), "question": itemgetter("question")}
            | ChatPromptTemplate.from_template(GENERATE_ANSWER_PROMPT)
            | self.__llm
            | StrOutputParser()
        )

        logging.info(f"[LLM] Executing prompt to answer query: {rag_chain}")
        output = rag_chain.invoke({"context": context, "question": question})
        logging.info(f"[LLM] Generated answer: {output}")

        return output
    
    def summarize(self, transcript: str, metadata: dict) -> str:
        generate_summary = (
            ChatPromptTemplate.from_template(GENERATE_VIDEO_SUMMARY)
            | self.__llm
            | StrOutputParser()
        )

        logging.info(f"[LLM] Executing prompt to summarize video content: {generate_summary}")
        output = generate_summary.invoke({
            "transcript": transcript,
            # "description": metadata["description"],
            # "auto": metadata["is_auto"]
        })
        return output
    
    def get_unique_union(self, documents: list[list]):
        flattened_docs = [dumps(doc) for sublist in documents for doc in sublist]
        unique_docs = list(set(flattened_docs))
        return [loads(doc) for doc in unique_docs]



