from youtube_handler import CaptionRetriever
import data_store
import util
import query_resolver
import os

util.init_logger()
util.load_env("server_config.env")
util.init_langsmith()

use_openai = os.getenv("USE_OPENAI") == "1"
if use_openai:
    db_name = "video_search_openai"
else:
    db_name = "video_search_ollama"

SEGMENT_LENGTH = 60

urls = [    
    # "https://www.youtube.com/watch?v=lPrjP4A_X4s", # krutz
    # "https://www.youtube.com/watch?v=nTq-OKy5kHs", # mitocw
    # "https://www.youtube.com/watch?v=R8uxmXmtOrk", # hotz
    # "https://www.youtube.com/watch?v=sq-SqqsTlbM", # peterson
    # "https://www.youtube.com/playlist?list=PLZES21J5RvsHOeSW9Vrvo0EEc2juNe3tX", # dp mitocw
    # "https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ", # andrej playlist
    # "https://www.youtube.com/playlist?list=PL0-GT3co4r2y2YErbmuJw2L5tW4Ew2O5B", # 3blue1brown playlist
    "https://www.youtube.com/playlist?list=PL8URkIfzUkcfwX7twgLYSzyMZGYF9Aihb", # naruto quotes playlist
    "https://www.youtube.com/watch?v=9tEuNRezlyI", # jiraiya speech
]

resolver = query_resolver.QueryResolver()

ds = data_store.VideoSearchDataStore(os.getenv("QDRANT_URL"), db_name, resolver.get_embedding_func())

# for url in urls:
#     print(url)
#     if CaptionRetriever.is_playlist(url):
#         caption_metadata_pairs = CaptionRetriever.get_english_captions_xml_playlist(url, is_already_in_db=ds.is_video_in_db)
#         print("playlist")
#         for caption, metadata in caption_metadata_pairs:
#             if caption is not None:
#                 print(metadata['title'])
#                 print(caption[:100])
#             else:
#                 print(f"{metadata['title']} is already in db or has no captions")
#         caption_metadata_pairs = list(filter(lambda x: x[0] is not None, caption_metadata_pairs))
#         ds.add_playlist_to_db(caption_metadata_pairs, summarize=resolver.summarize, segment_length=SEGMENT_LENGTH)

#     else:
#         caption, metadata = CaptionRetriever.get_english_captions_xml_video(url, is_already_in_db=ds.is_video_in_db)
#         print("video")

#         if caption is not None:
#             print(caption[:100])
#             ds.add_video_to_db(caption, metadata, resolver.summarize, SEGMENT_LENGTH)
#         else:
#             print(f"{metadata['title']} is already in db or has no captions")

query = "does IQ decline with age?"
query = "what happens if we live a modern, sedentary lifestyle?"
query = "What truly exists in reality?"
query = "who created the circumstances that caused Obito to despair?"
# query = "who stopped Gaara from killing destroying the world and all the people?"
# query = "Can there be hate between those who experienced the same pain?"

# query = "When does the determinant of a transformation matrix become zero?"
# query = "what happens when you scale up a vector and what does it mean?"

# query = "How can we optimize llm training in pytorch?"
# query = "What is distributed data parallel and how does it help in training large language models?"
# query = "What is flash attention and how does it help in training large language models?"
# query = "how to determine a good learning rate?"

# query = "What is the edit distance problem?"
# query = "Is there a three node tree example for which the greedy algorithm fails?"
# query = "where is the Dijkstra's algorithm used?"

# results = ds.search(query, 5)

# for result in results:
#     print(result.page_content)
#     print(result.metadata)
#     print("\n")

# results = []

# context = "\n".join([result.page_content for result in results])
answer = resolver.answer_question(query, ds)
print(answer)

