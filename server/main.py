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

urls = [    
    # "https://www.youtube.com/watch?v=lPrjP4A_X4s", # krutz
    # "https://www.youtube.com/watch?v=nTq-OKy5kHs", # mitocw
    # "https://www.youtube.com/watch?v=R8uxmXmtOrk", # hotz
    # "https://www.youtube.com/watch?v=sq-SqqsTlbM", # peterson
    "https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ", # andrej playlist
    # "https://www.youtube.com/playlist?list=PL0-GT3co4r2y2YErbmuJw2L5tW4Ew2O5B", # 3blue1brown playlist
    "https://www.youtube.com/playlist?list=PL8URkIfzUkcfwX7twgLYSzyMZGYF9Aihb", # naruto quotes playlist
]

resolver = query_resolver.QueryResolver()

ds = data_store.VideoSearchDataStore(os.getenv("QDRANT_URL"), db_name, resolver.get_embedding_func())

# for url in urls:
#     print(url)
#     if CaptionRetriever.is_playlist(url):
#         caption_metadata_pairs = CaptionRetriever.get_english_captions_xml_playlist(url)
#         print("playlist")
#         for caption, metadata in caption_metadata_pairs:
#             if caption is not None:
#                 print(metadata['title'])
#                 print(caption[:100], metadata)
#             else:
#                 print(f"{metadata['title']} has no captions")

#         ds.add_playlist_to_db(caption_metadata_pairs, 30)
#     else:
#         caption, metadata = CaptionRetriever.get_english_captions_xml_video(url)
#         print("video")
#         print(caption[:100], metadata)

#         ds.add_video_to_db(caption, metadata, 30)

query = "does IQ decline with age?"
query = "what happens if we live a modern, sedentary lifestyle?"
query = "What truly exists in reality?"
query = "who created the circumstances that caused Obito to despair?"
query = "who stopped Gaara from killing destroying the world and all the people?"
query = "Can there be hate between those who experienced the same pain?"

# query = "How can we optimize llm training in pytorch?"
# query = "What is distributed data parallel and how does it help in training large language models?"
# query = "What is flash attention and how does it help in training large language models?"

# results = ds.search(query, 5)

# for result in results:
#     print(result.page_content)
#     print(result.metadata)
#     print("\n")

# results = []

# context = "\n".join([result.page_content for result in results])
answer = resolver.answer_question(query, ds)
print(answer)

