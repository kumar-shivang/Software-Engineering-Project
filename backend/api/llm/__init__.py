import uuid

from flask import Blueprint, jsonify, request
from langchain_core.messages import AIMessage, HumanMessage

from .chat import code_model, code_prompt, qa_model, qa_prompt, with_message_history
from .store import get_session_history, save_session_history
from api import api
from database.tables import ProgrammingSubmission, Submission

llm_blueprint = Blueprint("/llm", __name__, url_prefix="/help")


# NOTE: chat with the chatbot
@llm_blueprint.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data["message"]

    if "session_id" in data and len(data["session_id"]) > 0:
        session_id = data["session_id"]
    else:
        session_id = uuid.uuid4().hex

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
    json = {
        "response": response.content,
        "session_id": session_id,
    }

    return jsonify(json)


# NOTE: Get explanation of code errors
@llm_blueprint.route("/explain", methods=["POST"])
def explain():
    data = request.json
    submission_id = data["submission_id"]
    submission = ProgrammingSubmission.objects(id=submission_id).first()
    if not submission:
        return jsonify({"error": "Submission not found"})
    code = submission.code
    question = submission.assignment.description
    prompt = code_prompt.format(code=code, question=question)
    response = code_model.invoke(prompt).content
    return jsonify({"data": response})


# NOTE: Get feedback from assignment submissions
@llm_blueprint.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    submission_id = data["submission_id"]
    submission = Submission.objects(id=submission_id).first()
    result = submission.get_result()
    response = dict()
    for q in result:
        _id = q["id"]
        question = q["question"]
        answer = q["answer"]
        correct = q["correct"]
        if correct:
            response[_id] = "Correct"
        else:
            new_prompt = qa_prompt.format(question=question, answer=answer)
            response[_id] = qa_model.invoke(new_prompt).content

    return jsonify({ "data": response })


api.register_blueprint(llm_blueprint)
