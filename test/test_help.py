import uuid


def test_chat(client):
    # Define the message to send
    message = "Say OK"
    session_id = str(uuid.uuid4())

    # Prepare the request data
    data = {"message": message, "session_id": session_id}

    # Send the POST request
    response = client.post("/api/help/chat", json=data)

    # Assertions
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json["session_id"] == session_id
    assert "ok" in response_json["response"].lower()


def test_explain_real_response(client):
    # Define the code and question to send
    code = "print('Hello, World!')"
    question = "What does this code print?"

    # Prepare the request data
    data = {"code": code, "question": question}

    # Send the POST request
    response = client.post("/api/help/explain", json=data)

    # Assertions
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json["response"]


def test_feedback_real_response(client):
    # Define the assignment data to send
    assignment = [
        {
            "id": "1",
            "question": "What is the capital of France?",
            "answer": "Paris",
            "correct": True,
        },
        {"id": "2", "question": "What is 2 + 2?", "answer": "5", "correct": False},
    ]

    # Prepare the request data
    data = {"assignment": assignment}

    # Send the POST request
    response = client.post("/api/help/feedback", json=data)

    # Assertions
    assert response.status_code == 200
    response_json = response.get_json()

    # Check for the expected response
    assert response_json["1"] == "Correct"
    assert response_json["2"]
