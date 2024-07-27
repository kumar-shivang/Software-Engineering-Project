import uuid

from flask import Blueprint, jsonify, request
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from .chat import code_model, code_prompt, qa_model, qa_prompt, with_message_history
from .store import get_session_history, save_session_history


llm = Blueprint("/llm", __name__)


@llm.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data["message"]

    session_id = data.get("session_id", str(uuid.uuid4()))

    config = {"configurable": {"session_id": session_id}}

    # Retrieve or create the session history
    history = get_session_history(session_id)

    # Append the new message to the history
    history.add_message(HumanMessage(message))

    # Process the chat with the message history (assuming with_message_history is a function)
    response = with_message_history.invoke(history.messages, config)

    history.add_ai_message(AIMessage(response.content))

    # Save the updated session history
    save_session_history(session_id, history)
    json = {"session_id": session_id, "response": response.content}

    return jsonify(json)


@llm.route("/explain", methods=["POST"])
def explain():
    data = request.json
    # message = data['message']
    code = data["code"]
    question = data["question"]
    prompt = code_prompt.format(code=code, question=question)
    response = code_model.invoke(prompt).content
    return jsonify({"response": response})


@llm.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    assignment = data["assignment"]
    response = dict()
    for q in assignment:
        id = q["id"]
        question = q["question"]
        answer = q["answer"]
        correct = q["correct"]
        if correct:
            response[id] = "Correct"
        else:
            new_prompt = qa_prompt.format(question=question, answer=answer)
            response[id] = qa_model.invoke(new_prompt).content
    return jsonify(response)
