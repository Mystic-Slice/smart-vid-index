from typing import List
from langchain_community.vectorstores.redis import Redis, RedisText, RedisNum, RedisTag
from langchain_community.vectorstores.redis.schema import read_schema
from langchain.docstore.document import Document
import logging
from .data_classes import Caption

class VideoSearchDataStore:
    def __init__(self, redis_url, index_name, schema_dir, embedding_func, segment_length=20):

        sample_metadata = {
            'author': 'TheRightMind', 
            'channel_url': 'https://www.youtube.com/channel/UC6q7LpU3nQm52vNkz-1MVFA', 
            'description': 'song', 
            'length': 150, 
            'title': 'Jordan Peterson Talks About His Own IQ', 
            'video_id': 'sq-SqqsTlbM'
        }

        # self.__video_datastore = Redis.from_documents(
        #     [Document(page_content="dummy", metadata=sample_metadata)],
        #     redis_url=redis_url,
        #     index_name=index_name + "_vid_store",
        #     embedding=embedding_func,
        # )
        # self.__caption_datastore = Redis.from_documents(
        #     [Document(page_content="dummy", metadata=sample_metadata)],
        #     redis_url=redis_url,
        #     index_name=index_name + "_caption_store",
        #     embedding=embedding_func,
        # )

        self.__video_datastore = Redis.from_existing_index(
            embedding=embedding_func,
            index_name=index_name + "_vid_store",
            schema=schema_dir + "datastore.yaml",
            redis_url=redis_url,
        )
        self.__caption_datastore = Redis.from_existing_index(
            embedding=embedding_func,
            index_name=index_name + "_caption_store",
            schema=schema_dir + "datastore.yaml",
            redis_url=redis_url,
        )

        self.__redis_url = redis_url
        self.__embedding_func = embedding_func
        self.__index_name = index_name
        self.__segment_length = segment_length
        logging.info(f"[{self.__class__.__name__}={self.__index_name}] DataStore initialized successfully")

    def add_video_to_db(self, xml_caption: str, metadata: dict) -> bool:
        if self.is_video_in_db(metadata["video_id"]):
            print("here")
            logging.info(f"[VideoSearchDataStore={self.__index_name}] Video already in DB")
            return False

        logging.info(f"[VideoSearchDataStore={self.__index_name}] Adding caption: {xml_caption[:100]}...")

        caption_list = Caption.parse_xml_caption(xml_caption)
        caption_list_merged = Caption.merge_captions(caption_list, self.__segment_length)
        texts = [caption.text for caption in caption_list_merged]
        metas = [
            {
                "start": caption.start,
                "duration": caption.duration,
                **metadata,
            }
            for caption in caption_list_merged
        ]
        documents = [Document(page_content=text, metadata=meta) for text, meta in zip(texts, metas)]

        ids = self.__caption_datastore.add_documents(documents)
        logging.info(f"[VideoSearchDataStore={self.__index_name}] Caption added successfully num_segments={len(ids)}")

        complete_transcript = " ".join(texts)
        vid_doc = Document(page_content=complete_transcript, metadata=metadata)

        ids = self.__video_datastore.add_documents([vid_doc])
        logging.info(f"[VideoSearchDataStore={self.__index_name}] Video added successfully ids={ids}")
        return True
    
    def is_video_in_db(self, video_id: str) -> bool:
        print(type(video_id), video_id)
        results = self.__video_datastore.similarity_search(query="adfs", filter=RedisText("video_id")==video_id, return_metadata=True)
        print([result.metadata for result in results])
        print(len(results))
        return results != []
    
    def search(self, query: str, num_results: int) -> List[dict]:
        print(self.__video_datastore.schema)
        logging.info(f"[VideoSearchDataStore={self.__index_name}] Searching for query: {query}")
        results = self.__caption_datastore.similarity_search(query, num_results, return_metadata=True)
        logging.info(f"[VideoSearchDataStore={self.__index_name}] Search completed successfully num_results={len(results)}")
        return results