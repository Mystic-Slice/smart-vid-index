import logging
import os
from flask import Flask, request

from youtube_handler import CaptionRetriever
import data_store
import util
import query_resolver

util.init_logger("logs/server.log")
util.load_env("server_config.env")
util.init_langsmith()

use_openai = os.getenv("USE_OPENAI") == "1"
if use_openai:
    db_name = "video_search_openai"
else:
    db_name = "video_search_ollama"

SEGMENT_LENGTH = 60

app = Flask(__name__)
app.secret_key = "dummy"

def get_resolver_ds():
    resolver = query_resolver.QueryResolver()
    ds = data_store.VideoSearchDataStore(os.getenv("QDRANT_URL"), db_name, resolver.get_embedding_func())
    return resolver, ds

@app.route("/")
def root():
    return { "message": "Hello World" }

@app.route("/search", methods=["POST"])
def search():
    resolver, ds = get_resolver_ds()

    query = request.json["query"]

    response = resolver.answer_question(query, ds)
    result = { "question": query, "response": response }
    return result

@app.route("/mock_search", methods=["POST"])
def mock_search():
    query = request.json["query"]
    response = {
        "answer": f"mock response to {query}",
        "links": ["https://www.youtube.com/embed/dQw4w9WgXcQ", "https://www.youtube.com/embed/3YxaaGgTQYM"]
    }
    result = { "question": query, "response": response }
    return result

@app.route("/all_titles")
def all_titles():
    _, ds = get_resolver_ds()
    return { "titles": ds.get_all_video_titles() }

@app.route("/all_metadata")
def all_metadata():
    _, ds = get_resolver_ds()
    return { "metadata": ds.get_all_vids() }

@app.route("/video")
def add_videos():
    url = request.args.get("url")

    resolver, ds = get_resolver_ds()

    msg = ""

    if CaptionRetriever.is_playlist(url):
        caption_metadata_pairs = CaptionRetriever.get_english_captions_xml_playlist(url, is_already_in_db=ds.is_video_in_db)
        for i, (caption, metadata) in enumerate(caption_metadata_pairs):
            if caption is not None:
                msg += f"{i+1}.{metadata['title']} added\n"
                # msg += caption[:100] + "\n"

                print(metadata['title'])
                print(caption[:100])
            else:
                msg += f"{i+1}.{metadata['title']} is already in db or has no captions\n"
                print(f"{metadata['title']} is already in db or has no captions")
        caption_metadata_pairs = list(filter(lambda x: x[0] is not None, caption_metadata_pairs))
        ds.add_playlist_to_db(caption_metadata_pairs, summarize=resolver.summarize, segment_length=SEGMENT_LENGTH)
        msg += "playlist added"
    else:
        caption, metadata = CaptionRetriever.get_english_captions_xml_video(url, is_already_in_db=ds.is_video_in_db)
        if caption is not None:
            msg += metadata['title'] + " added\n"
            # msg += caption[:100] + "\n"
            print(caption[:100])
            ds.add_video_to_db(caption, metadata, resolver.summarize, SEGMENT_LENGTH)
            msg += "video added"
        else:
            print(f"{metadata['title']} is already in db or has no captions")
            msg += "video already in db or has no captions"
    return { "message": msg }