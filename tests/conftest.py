"""
Pytest fixtures for FastAPI app tests.
Provides TestClient and sample test data.
"""

import pytest
from fastapi.testclient import TestClient
from src import app as app_module


# Store the original activities data
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Team-based soccer training and competitive matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["luke@mergington.edu", "mia@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Swim practice, technique improvement, and pool workouts",
        "schedule": "Mondays, Wednesdays, Fridays, 5:00 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["nina@mergington.edu", "sam@mergington.edu"]
    },
    "Art Club": {
        "description": "Creative projects in painting, drawing, and mixed media",
        "schedule": "Wednesdays, 3:30 PM - 4:45 PM",
        "max_participants": 16,
        "participants": ["ava@mergington.edu", "leo@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting workshops, stage production, and improvisation practice",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["zoe@mergington.edu", "ethan@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Advanced math problem solving and competition preparation",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["oliver@mergington.edu", "sophia@mergington.edu"]
    },
    "Science Research Club": {
        "description": "Student-led experiments, research projects, and science fairs",
        "schedule": "Tuesdays, 4:15 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["emma@mergington.edu", "jack@mergington.edu"]
    }
}


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Arrange: Reset the global activities dictionary before each test.
    This ensures test isolation - each test starts with fresh data.
    Autouse=True means this runs before every test automatically.
    """
    # Reset activities to original state before each test
    app_module.activities.clear()
    app_module.activities.update({k: {"participants": v["participants"][:], **{kk: vv for kk, vv in v.items() if kk != "participants"}} for k, v in ORIGINAL_ACTIVITIES.items()})
    yield
    # Cleanup after test (optional, but good practice)
    app_module.activities.clear()
    app_module.activities.update({k: {"participants": v["participants"][:], **{kk: vv for kk, vv in v.items() if kk != "participants"}} for k, v in ORIGINAL_ACTIVITIES.items()})


@pytest.fixture
def client():
    """
    Arrange: Create a TestClient for the FastAPI app.
    This fixture is used by all tests to make HTTP requests to the app.
    """
    return TestClient(app_module.app)


@pytest.fixture
def sample_activity_name():
    """
    Fixture providing a valid activity name for testing.
    """
    return "Chess Club"


@pytest.fixture
def sample_email():
    """
    Fixture providing a new student email for testing signup.
    """
    return "newstudent@mergington.edu"


@pytest.fixture
def existing_email():
    """
    Fixture providing an email already signed up for Chess Club.
    """
    return "michael@mergington.edu"
