"""
Global fixtures shared across the entire test suite.
"""
import pytest
from src.api_client import APIClient


@pytest.fixture(scope="session")
def client() -> APIClient:
    return APIClient()


@pytest.fixture(scope="session")
def auth_token(client: APIClient) -> str:
    response = client.post("/auth/login", json={
        "username": "emilys",
        "password": "emilyspass",
    })
    assert response.status_code == 200, f"Could not obtain auth token: {response.text}"
    return response.json()["accessToken"]


@pytest.fixture(scope="session")
def authenticated_client(auth_token: str) -> APIClient:
    return APIClient(token=auth_token)


@pytest.fixture
def created_user(client: APIClient) -> dict:
    response = client.post("/users/add", json={
        "firstName": "Test",
        "lastName": "User",
        "age": 25,
    })
    assert response.status_code == 201
    return response.json()


def pytest_configure(config):
    markers = [
        "smoke: Fast critical-path tests",
        "regression: Full regression suite",
        "auth: Authentication-related tests",
        "users: User CRUD tests",
        "resources: Resources endpoint tests",
        "negative: Negative/edge case tests",
        "performance: Response time assertions",
    ]
    for marker in markers:
        config.addinivalue_line("markers", marker)
