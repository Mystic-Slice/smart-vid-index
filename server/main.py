import youtube_handler
import data_store
import util
import llm
import os

util.init_logger()
util.load_env("server_config.env")

urls = [    
    "https://www.youtube.com/watch?v=lPrjP4A_X4s", # krutz
    "https://www.youtube.com/watch?v=nTq-OKy5kHs", # mitocw
    "https://www.youtube.com/watch?v=R8uxmXmtOrk", # hotz
    "https://www.youtube.com/watch?v=sq-SqqsTlbM", # peterson
]

ds = data_store.VideoSearchDataStore(os.getenv("QDRANT_URL"), "video_search", "data_store/schema/", llm.get_embedding_func(), 20)

for url in urls:
    print(url)
    sr = youtube_handler.CaptionRetriever(url)

    caption = sr.get_english_captions_xml()
    metadata = sr.get_meta_data()

    ds.add_video_to_db(caption, metadata)

query = "does IQ decline with age?"
query = "what happens if we live a modern, sedentary lifestyle?"
query = "what is a three phase inverter?"

results = ds.search(query, 5)

for result in results:
    print(result.page_content)
    print(result.metadata)
    print("\n")

