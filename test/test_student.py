from unittest.mock import MagicMock


def test_get_students(client, mocker):
    mock_students = [
        {"name": "John Doe", "email": "john@example.com", "password": "password"},
        {"name": "Jane Doe", "email": "jane@example.com", "password": "password"},
    ]
    mock_queryset = MagicMock()
    mock_queryset.to_json.return_value = mock_students
    mocker.patch("database.tables.Student.objects", return_value=mock_queryset)

    response = client.get("/api/student/")
    print(response)
    assert response.status_code == 200
    assert response.get_json() == mock_students


def test_get_student(client, mocker):
    # Mock student data
    student_id = "12345"
    mock_student = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password",
        "courses": [],
        "grades": {},
        "submissions": [],
    }

    # Create a mock for the student document
    mock_student_doc = MagicMock()
    mock_student_doc.to_json.return_value = mock_student

    # Patch the Student.objects(id=student_id).first() method
    mocker.patch(
        "database.tables.Student.objects",
        return_value=MagicMock(first=MagicMock(return_value=mock_student_doc)),
    )

    # Test with an existing student
    response = client.get(f"/api/student/{student_id}")
    assert response.status_code == 200
    assert response.get_json() == mock_student

    # Test with a non-existing student
    mocker.patch(
        "database.tables.Student.objects",
        return_value=MagicMock(first=MagicMock(return_value=None)),
    )
    response = client.get(f"/api/student/non_existing_id")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Student not found"}


def test_get_courses(client, mocker):
    # Mock student data
    student_id = "12345"
    mock_courses = [
        MagicMock(
            to_json=MagicMock(
                return_value={"name": "Math 101", "description": "Basic Math"}
            )
        ),
        MagicMock(
            to_json=MagicMock(
                return_value={"name": "History 101", "description": "World History"}
            )
        ),
    ]
    mock_student = MagicMock()
    mock_student.courses = mock_courses

    # Patch the Student.objects(id=student_id).first() method
    mocker.patch(
        "database.tables.Student.objects",
        return_value=MagicMock(first=MagicMock(return_value=mock_student)),
    )

    # Test with an existing student
    response = client.get(f"/api/student/courses/{student_id}")
    assert response.status_code == 200
    assert response.get_json() == {
        "courses": [course.to_json() for course in mock_courses]
    }

    # Test with a non-existing student
    mocker.patch(
        "database.tables.Student.objects",
        return_value=MagicMock(first=MagicMock(return_value=None)),
    )
    non_existing_student_id = "11111"
    response = client.get(f"/api/student/courses/{non_existing_student_id}")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Student not found"}


def test_get_score(client, mocker):
    # Mock student data
    student_id = "12345"
    assignment_id = "67890"
    mock_score = 95

    # Create a mock for the student document
    mock_student = MagicMock()
    mock_student.get_score.return_value = mock_score

    # Patch the Student.objects(id=student_id).first() method
    mocker.patch(
        "database.tables.Student.objects",
        return_value=MagicMock(first=MagicMock(return_value=mock_student)),
    )

    # Patch the Assignment.objects(id=assignment_id).first() method
    mocker.patch(
        "database.tables.Assignment.objects",
        return_value=MagicMock(first=MagicMock(return_value=True)),
    )

    # Test with an existing student and assignment
    response = client.get("/api/student/score", json={"student_id": student_id, "assignment_id": assignment_id})
    assert response.status_code == 200
    assert response.get_json() == {"score": mock_score}

    # Test with a non-existing student
    mocker.patch(
        "database.tables.Student.objects",
        return_value=MagicMock(first=MagicMock(return_value=None)),
    )
    response = client.get("/api/student/score", json={"student_id": "non_existing_id", "assignment_id": assignment_id})
    assert response.status_code == 404
    assert response.get_json() == {"error": "Student not found"}

    # Test with a non-existing assignment
    mocker.patch(
        "database.tables.Student.objects",
        return_value=MagicMock(first=MagicMock(return_value=mock_student)),
    )
    mocker.patch(
        "database.tables.Assignment.objects",
        return_value=MagicMock(first=MagicMock(return_value=None)),
    )
    response = client.get("/api/student/score", json={"student_id": student_id, "assignment_id": "non_existing_id"})
    assert response.status_code == 404
    assert response.get_json() == {"error": "Assignment not found"}


def test_submit(client, mocker):
    # Mock data
    student_id = "12345"
    assignment_id = "67890"
    answers = {"question1_id": ["answer1"], "question2_id": ["answer2"]}

    # Mock the student object
    mock_student = MagicMock()
    mock_student.submit = MagicMock()

    # Patch the Student.objects(id=student_id).first() method
    mocker.patch(
        "database.tables.Student.objects",
        return_value=MagicMock(first=MagicMock(return_value=mock_student)),
    )

    # Patch the Assignment.objects(id=assignment_id).first() method
    mock_assignment = MagicMock()
    mock_assignment.id = assignment_id  # Ensure assignment_id is correctly set
    mocker.patch(
        "database.tables.Assignment.objects",
        return_value=MagicMock(first=MagicMock(return_value=mock_assignment)),
    )

    # Test valid submission
    response = client.post("/api/student/submit",
                           json={"student_id": student_id, "assignment_id": assignment_id, "answers": answers})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Submitted"}
    mock_student.submit.assert_called_once_with(assignment_id, answers)
    # Test invalid student
    mocker.patch(
        "database.tables.Student.objects",
        return_value=MagicMock(first=MagicMock(return_value=None)),
    )
    response = client.post("/api/student/submit", json={"student_id": "invalid_student_id", "assignment_id": assignment_id, "answers": answers})
    assert response.status_code == 404
    assert response.get_json() == {"error": "Student not found"}

    # Test invalid assignment
    mocker.patch(
        "database.tables.Student.objects",
        return_value=MagicMock(first=MagicMock(return_value=mock_student)),
    )
    mocker.patch(
        "database.tables.Assignment.objects",
        return_value=MagicMock(first=MagicMock(return_value=None)),
    )
    response = client.post("/api/student/submit", json={"student_id": student_id, "assignment_id": "invalid_assignment_id", "answers": answers})
    assert response.status_code == 404
    assert response.get_json() == {"error": "Assignment not found"}

