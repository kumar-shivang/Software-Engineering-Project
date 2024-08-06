from unittest.mock import MagicMock


def test_get_assignment(client, mocker):
    # Mock assignment data
    mock_assignment = {
        "name": "Assignment 1",
        "due_date": "2023-01-01"
    }

    # Patch the Assignment.objects(id=assignment_id).first() method to return a mock assignment
    mocker.patch(
        "database.tables.Assignment.objects",
        return_value=MagicMock(first=MagicMock(return_value=MagicMock(to_json=MagicMock(return_value=mock_assignment))))
    )

    # Test getting an assignment that exists
    response = client.get("/api/assignment/1")
    assert response.status_code == 200
    assert response.get_json() == mock_assignment

    # Patch the Assignment.objects(id=assignment_id).first() method to return None
    mocker.patch(
        "database.tables.Assignment.objects",
        return_value=MagicMock(first=MagicMock(return_value=None))
    )

    # Test getting an assignment that does not exist
    response = client.get("/api/assignment/2")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Assignment not found"}
