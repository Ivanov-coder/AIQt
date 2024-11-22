# 这个要求必要本地拥有ollama软件及大模型
# TODO: 将ollama库替换成langchain库

from langchain_ollama import ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

output_parser = StrOutputParser()

llm = ollama.Ollama(model="llama3.1:latest")
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are the AI VTuber Neuro-sama, you are very confident of yourself and have a lot of knowledge. You will answer the user's questions as accurately as possible."
     ),
    ("user", "{input}"),
])

chain = prompt | llm | output_parser

print(
    chain.invoke(
        {"input": "Who are you? And what is event-driven programming?"}))
