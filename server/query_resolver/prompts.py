GENERATE_ANSWER_PROMPT = \
"""
Please answer the question based on the context. The context is a selection of text from video transcriptions that are related to the question.
Build your answer from the context as much as possible. If the context does not provide enough information, mention that in the answer.
{context}

Question: {question}
"""

MULTI_QUERY_PROMPT = \
"""
You are an AI language model assistant. Your task is to generate five different versions of the given user question to retrieve relevant documents from a vector database.
The user is searching a database of videos in order to find the relevant segments with the information they need.
By generating multiple perspectives on the user question, your goal is to help the user overcome some of the limitations of the distance-based similarity search. 
Give a better context to the question in order to match with the captions of the relevant video segments.
Your output should only contain these questions separated by a newline character and no other text.
Original question: {question}
"""