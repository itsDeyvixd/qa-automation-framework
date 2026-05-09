"""
Tests for /auth/login endpoint — DummyJSON.
"""
import pytest
from src.api_client import APIClient
from src.schemas.api_schemas import LOGIN_SUCCESS_RESPONSE
from src.utils.assertions import (
    assert_ok, assert_schema,
    assert_response_time, assert_json_key,
)
from src.utils.data_factory import AuthFactory


@pytest.mark.smoke
@pytest.mark.auth
class TestLogin:

    def test_login_valid_credentials_returns_200(self, client: APIClient):
        assert_ok(client.post("/auth/login", json=AuthFactory.VALID_LOGIN))

    def test_login_returns_access_token(self, client: APIClient):
        body = client.post("/auth/login", json=AuthFactory.VALID_LOGIN).json()
        assert_json_key(body, "accessToken")

    def test_login_returns_refresh_token(self, client: APIClient):
        body = client.post("/auth/login", json=AuthFactory.VALID_LOGIN).json()
        assert_json_key(body, "refreshToken")

    def test_login_schema_is_valid(self, client: APIClient):
        assert_schema(client.post("/auth/login", json=AuthFactory.VALID_LOGIN).json(), LOGIN_SUCCESS_RESPONSE)

    def test_login_token_is_non_empty_string(self, client: APIClient):
        token = client.post("/auth/login", json=AuthFactory.VALID_LOGIN).json()["accessToken"]
        assert isinstance(token, str) and len(token) > 0

    def test_login_returns_user_info(self, client: APIClient):
        body = client.post("/auth/login", json=AuthFactory.VALID_LOGIN).json()
        for field in ("id", "username", "email", "firstName", "lastName"):
            assert field in body, f"Missing field: {field}"

    @pytest.mark.negative
    def test_login_invalid_credentials_returns_400(self, client: APIClient):
        response = client.post("/auth/login", json=AuthFactory.invalid_credentials())
        assert response.status_code in (400, 401)

    @pytest.mark.negative
    def test_login_invalid_credentials_has_error_message(self, client: APIClient):
        body = client.post("/auth/login", json=AuthFactory.invalid_credentials()).json()
        assert "message" in body

    @pytest.mark.negative
    def test_login_missing_password_returns_error(self, client: APIClient):
        response = client.post("/auth/login", json=AuthFactory.missing_password())
        assert response.status_code in (400, 401)

    @pytest.mark.negative
    def test_login_empty_body_returns_error(self, client: APIClient):
        response = client.post("/auth/login", json={})
        assert response.status_code in (400, 401)

    @pytest.mark.performance
    def test_login_response_time(self, client: APIClient):
        assert_response_time(client.post("/auth/login", json=AuthFactory.VALID_LOGIN))
