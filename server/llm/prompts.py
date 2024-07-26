GENERATE_ANSWER_PROMPT = """
    Please answer the question based on the context. The context is a selection of text from video transcriptions that are related to the question.
    Build your answer from the context as much as possible. If the context does not provide enough information, mention that in the answer.
    {context}

    Question: {question}
"""