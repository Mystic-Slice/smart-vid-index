import re
from typing import Callable, List, Optional, Tuple
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain.docstore.document import Document
import logging
from .data_classes import Caption

import html

class VideoSearchDataStore:
    def __init__(self, qdrant_url, collection_name, embedding_func):

        sample_metadata = {
            'author': '', 
            'channel_url': '', 
            'description': '', 
            'length': 0, 
            'title': '', 
            'video_id': '',
            'video_url': '',
        }
        self.__collection_name = collection_name
        self.__segment_length = 30
        self.__qdrant_client = QdrantClient(url=qdrant_url)

        try:
            logging.info(f"[{self.__class__.__name__}={self.__collection_name}] Attempting to connect to existing collections.")
            self.__video_datastore = QdrantVectorStore.from_existing_collection(
                url=qdrant_url,
                collection_name=self.get_vid_datastore_name(),
                embedding=embedding_func,
            )
            self.__caption_datastore = QdrantVectorStore.from_existing_collection(
                url=qdrant_url,
                collection_name=self.get_caption_datastore_name(),
                embedding=embedding_func,
            )
        except:    
            logging.info(f"[{self.__class__.__name__}={self.__collection_name}] No existing collections found. Creating new collections.")
            self.__video_datastore = QdrantVectorStore.from_documents(
                [Document(page_content="collection_creation", metadata=sample_metadata)],
                url=qdrant_url,
                collection_name=collection_name + "_vid_store",
                embedding=embedding_func,
            )
            self.__caption_datastore = QdrantVectorStore.from_documents(
                [Document(page_content="collection_creation", metadata=sample_metadata)],
                url=qdrant_url,
                collection_name=collection_name + "_caption_store",
                embedding=embedding_func,
            )

        logging.info(f"[{self.__class__.__name__}={self.__collection_name}] DataStore initialized successfully")

    def get_vid_datastore_name(self):
        return self.__collection_name + "_vid_store"
    
    def get_caption_datastore_name(self):
        return self.__collection_name + "_caption_store"

    def get_all_vids(self):
        points = self.__qdrant_client.scroll(
            collection_name=self.get_vid_datastore_name(),
            with_payload=True, 
            with_vectors=False,
            limit=self.__qdrant_client.count(self.__collection_name + "_vid_store").count
        )[0]

        metadatas = [point.payload["metadata"] for point in points]

        return metadatas
    
    def get_all_video_titles(self):
        return [metadata["title"] for metadata in self.get_all_vids()]

    def add_playlist_to_db(
        self, 
        caption_data: List[Tuple[str, dict]], 
        summarize: Optional[Callable[[str, dict], str]] = None, 
        segment_length: Optional[int] = None
    ) -> bool:
        if segment_length is not None:
            self.__segment_length = segment_length

        logging.info(f"[VideoSearchDataStore={self.__collection_name}] Adding playlist with {len(caption_data)} videos to DB")
        for i, (xml_caption, metadata) in enumerate(caption_data):
            logging.info(f"[VideoSearchDataStore={self.__collection_name}] Adding video {i+1}/{len(caption_data)}")
            self.add_video_to_db(xml_caption, metadata, summarize)
        return True

    def add_video_to_db(
        self, 
        xml_caption: str, 
        metadata: dict, 
        summarize: Optional[Callable[[str, dict], str]] = None, 
        segment_length: Optional[int] = None
    ) -> bool:
        if segment_length is not None:
            self.__segment_length = segment_length

        if self.is_video_in_db(metadata["video_id"]):
            logging.info(f"[VideoSearchDataStore={self.__collection_name}] Video {metadata['video_id']} already in DB")
            return False

        logging.info(f"[VideoSearchDataStore={self.__collection_name}] Adding caption: {xml_caption[:100]}...")

        caption_list = Caption.parse_xml_caption(xml_caption)
        caption_list_merged = Caption.merge_captions(caption_list, self.__segment_length)
        texts = [self.clean_text(caption.text, remove_annots=True) for caption in caption_list_merged]
        metas = [
            {
                "start": caption.start,
                "duration": caption.duration,
                **metadata,
            }
            for caption in caption_list_merged
        ]
        documents = [Document(page_content=text, metadata=meta) for text, meta in zip(texts, metas) if not text == ""]

        print(documents)

        ids = self.__caption_datastore.add_documents(documents)
        logging.info(f"[VideoSearchDataStore={self.__collection_name}] Caption added successfully num_segments={len(ids)}")

        complete_transcript = " ".join([caption.text for caption in caption_list])
        if summarize is not None:
            complete_transcript = summarize(complete_transcript, metadata)
        vid_doc = Document(page_content=complete_transcript, metadata=metadata)

        ids = self.__video_datastore.add_documents([vid_doc])
        logging.info(f"[VideoSearchDataStore={self.__collection_name}] Video {metadata['video_id']} added successfully ids={ids}")
        return True
    
    def is_video_in_db(self, video_id: str) -> bool:
        results = self.__video_datastore.similarity_search(
            query=" ", 
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.video_id",
                        match=models.MatchValue(
                            value=video_id
                        )
                    )
                ]
            ),
            k=1,
        )
        return results != []
    
    def delete_video(self, video_id: str) -> bool:
        logging.info(f"[VideoSearchDataStore={self.__collection_name}] Deleting video {video_id}")

        filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="metadata.video_id",
                    match=models.MatchValue(
                        value=video_id
                    )
                )
            ]
        )

        out = self.__qdrant_client.delete(
            collection_name=self.get_vid_datastore_name(),
            points_selector=filter,
        )
        out = self.__qdrant_client.delete(
            collection_name=self.get_caption_datastore_name(),
            points_selector=filter,
        )
        return out
    
    def clean_text(self, text: str, remove_annots = True) -> str:
        # Covert html entities to unicode
        text = html.unescape(text)

        # Remove newlines
        text = text.replace("\n", " ")

        if remove_annots:
            # Remove annotations like [Music], etc... in captions
            text = re.sub(r"\[.*?\]", "", text)

        return text

    # def search(self, query: str, num_results: int) -> List[dict]:
    #     query = self.clean_text(query, remove_annots=False)

    #     logging.info(f"[VideoSearchDataStore={self.__collection_name}] Searching for query: {query}")
    #     results = self.__caption_datastore.similarity_search(query, k=num_results)
    #     logging.info(f"[VideoSearchDataStore={self.__collection_name}] Search completed successfully num_results={len(results)}")
    #     return results
    
    def get_video_retriever(self, search_kwargs: dict):
        return self.__video_datastore.as_retriever(search_kwargs=search_kwargs)
    
    def get_caption_retriever(self, search_kwargs: dict):
        return self.__caption_datastore.as_retriever(search_kwargs=search_kwargs)