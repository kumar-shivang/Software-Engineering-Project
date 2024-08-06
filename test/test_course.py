from unittest.mock import MagicMock


def test_get_courses(client, mocker):
    # Patch the Course.objects().to_json() method to return an empty list
    mocker.patch(
        "database.tables.Course.objects",
        return_value=MagicMock(to_json=MagicMock(return_value=list())),
    )

    # Test getting all courses when no courses are found
    response = client.get("/api/course/")
    assert response.status_code == 404
    assert response.get_json() == {"error": "No courses found"}
    # Mock course data
    mock_courses = [
        {"name": "Math 101", "description": "Basic Math"},
        {"name": "History 101", "description": "World History"},
    ]

    # Patch the Course.objects().to_json() method to return mock courses
    mocker.patch(
        "database.tables.Course.objects",
        return_value=MagicMock(to_json=MagicMock(return_value=mock_courses)),
    )

    # Test getting all courses
    response = client.get("/api/course/")
    assert response.status_code == 200
    assert response.get_json() == mock_courses


def test_get_course(client, mocker):
    # Mock course data
    mock_course = {"name": "Math 101", "description": "Basic Math"}

    # Patch the Course.objects(id=course_id).first() method to return a mock course
    mocker.patch(
        "database.tables.Course.objects",
        return_value=MagicMock(first=MagicMock(return_value=MagicMock(to_json=MagicMock(return_value=mock_course))))
    )

    # Test getting a course that exists
    response = client.get("/api/course/1")
    assert response.status_code == 200
    assert response.get_json() == mock_course

    # Patch the Course.objects(id=course_id).first() method to return None
    mocker.patch(
        "database.tables.Course.objects",
        return_value=MagicMock(first=MagicMock(return_value=None))
    )

    # Test getting a course that does not exist
    response = client.get("/api/course/2")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Course not found"}


def test_get_students(client, mocker):
    # Mock student data
    mock_students = [
        {"name": "John Doe", "email": "john@example.com"},
        {"name": "Jane Doe", "email": "jane@example.com"}
    ]

    # Patch the Course.objects(id=course_id).first() method to return a mock course with students
    mock_course = MagicMock(students=[MagicMock(to_json=MagicMock(return_value=student)) for student in mock_students])
    mocker.patch(
        "database.tables.Course.objects",
        return_value=MagicMock(first=MagicMock(return_value=mock_course))
    )

    # Test getting students for a course that exists
    response = client.get("/api/course/students/1")
    assert response.status_code == 200
    assert response.get_json() == {"students": mock_students}

    # Patch the Course.objects(id=course_id).first() method to return None
    mocker.patch(
        "database.tables.Course.objects",
        return_value=MagicMock(first=MagicMock(return_value=None))
    )

    # Test getting students for a course that does not exist
    response = client.get("/api/course/students/2")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Course not found"}

# TODO: Add tests for get_assignments and get_weeks routes