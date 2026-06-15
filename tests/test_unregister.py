"""
Tests for the unregister endpoint (DELETE /activities/{activity_name}/unregister).
Uses AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestUnregisterEndpoint:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_successful_for_registered_student(
        self, client, sample_activity_name, sample_email
    ):
        """
        Test successful unregister of a student from an activity.

        Arrange: Sign up a student, then prepare to unregister
        Act: Make DELETE request to unregister endpoint
        Assert: Verify unregister returns success message and status 200
        """
        # Arrange
        activity = sample_activity_name
        email = sample_email
        # First, sign up the student
        client.post(f"/activities/{activity}/signup", params={"email": email})

        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_unregister_removes_email_from_participants(
        self, client, sample_activity_name, sample_email
    ):
        """
        Test that unregister actually removes the email from participants list.

        Arrange: Sign up a student
        Act: Unregister the student, then retrieve activities
        Assert: Verify email no longer appears in participants list
        """
        # Arrange
        activity = sample_activity_name
        email = sample_email
        # First, sign up the student
        client.post(f"/activities/{activity}/signup", params={"email": email})

        # Act
        unregister_response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email},
        )
        activities_response = client.get("/activities")

        # Assert
        assert unregister_response.status_code == 200
        activities = activities_response.json()
        assert email not in activities[activity]["participants"]

    def test_unregister_fails_when_activity_not_found(self, client, sample_email):
        """
        Test that unregister fails with 404 when activity doesn't exist.

        Arrange: Prepare invalid activity name and student email
        Act: Make DELETE request to unregister with invalid activity
        Assert: Verify response is 404 with appropriate error message
        """
        # Arrange
        invalid_activity = "Nonexistent Club"
        email = sample_email

        # Act
        response = client.delete(
            f"/activities/{invalid_activity}/unregister",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_fails_when_not_signed_up(self, client, sample_activity_name, sample_email):
        """
        Test that unregister fails with 400 when student is not signed up.

        Arrange: Prepare activity and email that are not associated
        Act: Make DELETE request to unregister with email not in participants
        Assert: Verify response is 400 with appropriate error message
        """
        # Arrange
        activity = sample_activity_name
        email = sample_email  # Not signed up for this activity

        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"]

    def test_unregister_existing_participant(self, client, sample_activity_name, existing_email):
        """
        Test that we can unregister an existing participant.

        Arrange: Use activity and email already associated (Chess Club has michael@mergington.edu)
        Act: Make DELETE request to unregister
        Assert: Verify email is removed from participants list
        """
        # Arrange
        activity = sample_activity_name
        email = existing_email

        # Act
        unregister_response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email},
        )
        activities_response = client.get("/activities")

        # Assert
        assert unregister_response.status_code == 200
        activities = activities_response.json()
        assert email not in activities[activity]["participants"]

    def test_signup_then_unregister_then_signup_again(
        self, client, sample_activity_name, sample_email
    ):
        """
        Test that a student can sign up, unregister, and sign up again.

        Arrange: Prepare activity and email
        Act: Sign up -> Unregister -> Sign up again
        Assert: Verify final state has email in participants
        """
        # Arrange
        activity = sample_activity_name
        email = sample_email

        # Act - Sign up
        signup1 = client.post(f"/activities/{activity}/signup", params={"email": email})
        activities1 = client.get("/activities").json()

        # Act - Unregister
        unregister = client.delete(
            f"/activities/{activity}/unregister", params={"email": email}
        )
        activities2 = client.get("/activities").json()

        # Act - Sign up again
        signup2 = client.post(f"/activities/{activity}/signup", params={"email": email})
        activities3 = client.get("/activities").json()

        # Assert
        assert signup1.status_code == 200
        assert email in activities1[activity]["participants"]
        assert unregister.status_code == 200
        assert email not in activities2[activity]["participants"]
        assert signup2.status_code == 200
        assert email in activities3[activity]["participants"]
