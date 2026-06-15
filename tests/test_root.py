"""
Tests for the root endpoint (GET /).
Uses AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestRootEndpoint:
    """Tests for GET / endpoint"""

    def test_root_redirects_to_static_index(self, client):
        """
        Test that GET / redirects to the static index.html page.

        Arrange: TestClient is already initialized
        Act: Make GET request to /
        Assert: Verify redirect status code and location header
        """
        # Arrange
        expected_status = 307  # Temporary redirect

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == expected_status
        assert "/static/index.html" in response.headers.get("location", "")
