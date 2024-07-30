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

GENERATE_VIDEO_SUMMARY = \
"""
As a professional summarizer, create a concise and comprehensive summary of the provided text, which is a transcription of a video, for later retrieval using a distance-based similarity search while adhering to these guidelines:
1. Craft a summary of the `Transcript` that is detailed, thorough, in-depth, and complex, while maintaining clarity and conciseness. Do not speak in a third person perspective.
2. Incorporate main ideas and essential information, eliminating extraneous language and focusing on critical aspects.
3. Rely strictly on the provided text, without including external information.
4. Format the summary in paragraph form for easy understanding.
5. Make sure to keep the important keywords mentioned in the `Transcript`.
By following this optimized prompt, you will generate an effective summary that encapsulates the essence of the given text in a clear, concise, and reader-friendly manner.
`Transcript`: {transcript}
"""

# GENERATE_VIDEO_SUMMARY = \
# """
# As a professional summarizer, create a concise and comprehensive summary of the provided text, which is a transcription of a video, for later retrieval using a distance-based similarity search while adhering to these guidelines:
# 1. Craft a summary of the `Transcript` that is detailed, thorough, in-depth, and complex, while maintaining clarity and conciseness. Do not speak in a third person perspective.
# 2. Incorporate main ideas and essential information, eliminating extraneous language and focusing on critical aspects.
# 3. Rely strictly on the provided text, without including external information.
# 4. Format the summary in paragraph form for easy understanding.
# 5. Include any relevant information from the `Video Description` but ignore it if it is not pertinent to the video content.
# 6. Make sure to keep the important keywords mentioned in the `Transcript`.
# 7. If `Auto` is true, the transcript is an auto generated caption which may contain spelling  mistakes and other errors. Correct for it as needed.
# By following this optimized prompt, you will generate an effective summary that encapsulates the essence of the given text in a clear, concise, and reader-friendly manner.
# `Transcript`: {transcript}
# """