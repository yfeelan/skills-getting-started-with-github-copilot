"""
Tests for the activities endpoint (GET /activities).
Uses AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestActivitiesEndpoint:
    """Tests for GET /activities endpoint"""

    def test_get_all_activities_returns_correct_structure(self, client):
        """
        Test that GET /activities returns all activities with correct structure.

        Arrange: TestClient is ready
        Act: Make GET request to /activities
        Assert: Verify response contains all expected activities and structure
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Swimming Club",
            "Art Club",
            "Drama Club",
            "Math Olympiad",
            "Science Research Club",
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) == len(expected_activities)

    def test_activity_has_required_fields(self, client):
        """
        Test that each activity has required fields.

        Arrange: TestClient is ready
        Act: Make GET request to /activities
        Assert: Verify each activity has description, schedule, max_participants, participants
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict)
            assert required_fields.issubset(activity_data.keys()), (
                f"Activity {activity_name} missing fields. "
                f"Expected: {required_fields}, Got: {activity_data.keys()}"
            )
            assert isinstance(activity_data["participants"], list)

    def test_activities_have_participants(self, client):
        """
        Test that activities contain participant emails.

        Arrange: TestClient is ready
        Act: Make GET request to /activities
        Assert: Verify each activity has at least one participant
        """
        # Arrange - no specific setup needed

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            participants = activity_data["participants"]
            assert len(participants) > 0, f"Activity {activity_name} has no participants"
            assert all(isinstance(email, str) for email in participants), (
                f"Activity {activity_name} has non-string participants"
            )
