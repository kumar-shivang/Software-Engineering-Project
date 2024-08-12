from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import ChatOllama

from .store import get_session_history


chat_model = ChatOllama(
    model="qwen:0.5b",
    temperature=0.5,
    max_tokens=100,
    top_p=0.7,
    frequency_penalty=1,
    presence_penalty=1,
    stop=["\n"],
)

qa_model = ChatOllama(
    model="phi3:mini",
    temperature=1,
    max_tokens=100,
    top_p=0.7,
    frequency_penalty=1,
    presence_penalty=1,
    stop=["\n"],
)

code_model = ChatOllama(
    model="deepseek-coder",
    temperature=0.5,
    max_tokens=100,
    top_p=0.7,
    frequency_penalty=1,
    presence_penalty=1,
    stop=["\n"],
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Only answer questions related to programming. You can only use python language in your responses. You must refuse to answer anything else",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


qa_template = """Explain why the answer to a question is correct or incorrect.
Question: {question},
Answer: {answer}"""

code_template = """The code submitted to you is a wrong answer to the given question. Assist the student to understand why the code is wrong.
Question: {question},
Code: {code}"""


qa_prompt = PromptTemplate(template=qa_template, input_variables={"question", "answer"})
code_prompt = PromptTemplate(
    template=code_template, input_variables={"question", "code"}
)

chain = prompt | chat_model


with_message_history = RunnableWithMessageHistory(chain, get_session_history)
