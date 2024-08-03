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

resolver = None
ds = None

app = Flask(__name__)
app.secret_key = "dummy"

@app.route("/")
def root():
    return { "message": "Hello World" }

@app.route("/question")
def answer_question():
    resolver = query_resolver.QueryResolver()
    ds = data_store.VideoSearchDataStore(os.getenv("QDRANT_URL"), db_name, resolver.get_embedding_func())

    q = request.args.get("q")

    answer = resolver.answer_question(q, ds)
    print("here", answer)
    return { "question": q, "answer": answer }