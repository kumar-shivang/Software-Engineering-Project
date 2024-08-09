from unittest.mock import MagicMock


def test_get_week(client, mocker):
    # Mock week data with correct attributes
    mock_week = {"number": 1, "course": "Course 1", "assignments": [], "lectures": []}

    # Patch the Week.objects(id=week_id).first() method to return a mock week
    mocker.patch(
        "database.tables.Week.objects",
        return_value=MagicMock(
            first=MagicMock(
                return_value=MagicMock(to_json=MagicMock(return_value=mock_week))
            )
        ),
    )

    # Test getting a week that exists
    response = client.get("/api/week/1")
    assert response.status_code == 200
    assert response.get_json() == mock_week

    # Patch the Week.objects(id=week_id).first() method to return None
    mocker.patch(
        "database.tables.Week.objects",
        return_value=MagicMock(first=MagicMock(return_value=None)),
    )

    # Test getting a week that does not exist
    response = client.get("/api/week/2")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Week not found"}


def test_get_assignments(client, mocker):
    # Mock assignment data
    mock_assignments = [
        {"name": "Assignment 1", "due_date": "2023-01-01"},
        {"name": "Assignment 2", "due_date": "2023-01-08"},
    ]

    # Patch the Week.objects(id=week_id).first() method to return a mock week with assignments
    mock_week = MagicMock(
        assignments=[
            MagicMock(to_json=MagicMock(return_value=assignment))
            for assignment in mock_assignments
        ]
    )
    mocker.patch(
        "database.tables.Week.objects",
        return_value=MagicMock(first=MagicMock(return_value=mock_week)),
    )

    # Test getting assignments for a week that exists
    response = client.get("/api/week/assignments/1")
    assert response.status_code == 200
    assert response.get_json() == {"assignments": mock_assignments}

    # Patch the Week.objects(id=week_id).first() method to return None
    mocker.patch(
        "database.tables.Week.objects",
        return_value=MagicMock(first=MagicMock(return_value=None)),
    )

    # Test getting assignments for a week that does not exist
    response = client.get("/api/week/assignments/2")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Week not found"}
