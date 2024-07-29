def init_langsmith():
    import os
    os.environ['LANGCHAIN_TRACING_V2'] = 'true'