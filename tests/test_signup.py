"""
Tests for the signup endpoint (POST /activities/{activity_name}/signup).
Uses AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_successful_for_new_student(self, client, sample_activity_name, sample_email):
        """
        Test successful signup of a new student for an activity.

        Arrange: Prepare activity name and student email
        Act: Make POST request to signup endpoint
        Assert: Verify signup returns success message and status 200
        """
        # Arrange
        activity = sample_activity_name
        email = sample_email

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_signup_adds_email_to_participants(
        self, client, sample_activity_name, sample_email
    ):
        """
        Test that signup actually adds the email to participants list.

        Arrange: Prepare activity name and student email
        Act: Signup student, then retrieve activities
        Assert: Verify email appears in participants list
        """
        # Arrange
        activity = sample_activity_name
        email = sample_email

        # Act
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email},
        )
        activities_response = client.get("/activities")

        # Assert
        assert signup_response.status_code == 200
        activities = activities_response.json()
        assert email in activities[activity]["participants"]

    def test_signup_fails_when_activity_not_found(self, client, sample_email):
        """
        Test that signup fails with 404 when activity doesn't exist.

        Arrange: Prepare invalid activity name and student email
        Act: Make POST request to signup with invalid activity
        Assert: Verify response is 404 with appropriate error message
        """
        # Arrange
        invalid_activity = "Nonexistent Club"
        email = sample_email

        # Act
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_fails_when_already_signed_up(self, client, sample_activity_name, existing_email):
        """
        Test that signup fails with 400 when student is already signed up.

        Arrange: Use activity and email that are already associated
        Act: Make POST request to signup with already-registered email
        Assert: Verify response is 400 with appropriate error message
        """
        # Arrange
        activity = sample_activity_name
        email = existing_email  # Already in Chess Club's participants

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]

    def test_signup_multiple_different_students(self, client, sample_activity_name):
        """
        Test that multiple different students can sign up for same activity.

        Arrange: Prepare multiple unique email addresses
        Act: Sign up each student for the activity
        Assert: Verify all emails are added to participants
        """
        # Arrange
        activity = sample_activity_name
        emails = [
            "student1@mergington.edu",
            "student2@mergington.edu",
            "student3@mergington.edu",
        ]

        # Act
        responses = [
            client.post(f"/activities/{activity}/signup", params={"email": email})
            for email in emails
        ]
        activities = client.get("/activities").json()

        # Assert
        for response in responses:
            assert response.status_code == 200
        for email in emails:
            assert email in activities[activity]["participants"]
