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
    # model = "phi3:mini",
    # temperature=0.5,
    # max_tokens=100,
    top_p=0.7,
    frequency_penalty=1,
    presence_penalty=1,
    stop=["\n"],
)

qa_model = ChatOllama(
    model="phi3:mini",
    temperature=0.5,
    max_tokens=100,
    top_p=0.7,
    frequency_penalty=1,
    presence_penalty=1,
    # stop=["\n"],
)

code_model = ChatOllama(
    model="coder",
    temperature=0.5,
    max_tokens=200,
    top_p=0.7,
    frequency_penalty=1,
    presence_penalty=1,
    # stop=["\n"],
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


qa_template = """Evaluate the provided answer to the following question. Explain whether the answer is correct or incorrect, and provide a clear justification for your evaluation.

Question: {question}
Answer: {answer}

If the answer is incorrect or incomplete, identify the mistakes or missing information and suggest how the answer can be improved. Keep the answer concise and to the point and under 100 words."""

code_template = """The following code submitted by the student does not correctly solve the problem. Please provide detailed feedback to help the student understand the mistakes and guide them towards the correct solution.

Question: {question}
Code: {code}

Identify the errors or misconceptions in the code, explain why the code doesn't work as expected, and suggest improvements or corrections."""


qa_prompt = PromptTemplate(template=qa_template, input_variables={"question", "answer"})
code_prompt = PromptTemplate(
    template=code_template, input_variables={"question", "code"}
)

chain = prompt | chat_model


with_message_history = RunnableWithMessageHistory(chain, get_session_history)
