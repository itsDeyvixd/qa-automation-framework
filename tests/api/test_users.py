"""
Tests for /users endpoints — DummyJSON.
"""
import pytest
from src.api_client import APIClient
from src.schemas.api_schemas import (
    USER_LIST_RESPONSE, USER_OBJECT,
    CREATE_USER_RESPONSE, UPDATE_USER_RESPONSE, DELETE_USER_RESPONSE,
)
from src.utils.assertions import (
    assert_ok, assert_created, assert_not_found,
    assert_schema, assert_response_time, assert_list_not_empty,
    assert_status,  # <- borra assert_json_key de aquí
)
from src.utils.data_factory import UserFactory


@pytest.mark.smoke
@pytest.mark.users
class TestGetUsers:

    def test_list_users_returns_200(self, client: APIClient):
        assert_ok(client.get("/users"))

    def test_list_users_schema_is_valid(self, client: APIClient):
        assert_schema(client.get("/users").json(), USER_LIST_RESPONSE)

    def test_list_users_contains_data(self, client: APIClient):
        assert_list_not_empty(client.get("/users").json()["users"], "users")

    def test_list_users_has_pagination_fields(self, client: APIClient):
        body = client.get("/users").json()
        for field in ("total", "skip", "limit"):
            assert field in body

    def test_list_users_limit_param(self, client: APIClient):
        body = client.get("/users", params={"limit": 5}).json()
        assert len(body["users"]) <= 5

    def test_list_users_skip_param(self, client: APIClient):
        body = client.get("/users", params={"skip": 5}).json()
        assert body["skip"] == 5

    @pytest.mark.performance
    def test_list_users_response_time(self, client: APIClient):
        assert_response_time(client.get("/users"))


@pytest.mark.smoke
@pytest.mark.users
class TestGetSingleUser:

    def test_get_user_returns_200(self, client: APIClient):
        assert_ok(client.get("/users/1"))

    def test_get_user_schema_is_valid(self, client: APIClient):
        assert_schema(client.get("/users/1").json(), USER_OBJECT)

    def test_get_user_returns_correct_id(self, client: APIClient):
        assert client.get("/users/2").json()["id"] == 2

    def test_get_user_email_format(self, client: APIClient):
        email = client.get("/users/1").json()["email"]
        assert "@" in email and "." in email

    def test_get_user_image_is_url(self, client: APIClient):
        image = client.get("/users/1").json().get("image", "")
        assert image.startswith("https://"), f"Image should be HTTPS URL, got: {image}"

    @pytest.mark.negative
    def test_get_nonexistent_user_returns_404(self, client: APIClient):
        assert_not_found(client.get("/users/99999"))

    @pytest.mark.performance
    def test_get_single_user_response_time(self, client: APIClient):
        assert_response_time(client.get("/users/1"))


@pytest.mark.regression
@pytest.mark.users
class TestCreateUser:

    def test_create_user_returns_201(self, client: APIClient):
        assert_created(client.post("/users/add", json=UserFactory.valid_payload()))

    def test_create_user_schema_is_valid(self, client: APIClient):
        assert_schema(client.post("/users/add", json=UserFactory.valid_payload()).json(), CREATE_USER_RESPONSE)

    def test_create_user_returns_sent_first_name(self, client: APIClient):
        payload = UserFactory.valid_payload()
        body = client.post("/users/add", json=payload).json()
        assert body["firstName"] == payload["firstName"]

    def test_create_user_assigns_id(self, client: APIClient):
        body = client.post("/users/add", json=UserFactory.valid_payload()).json()
        assert "id" in body and body["id"]


@pytest.mark.regression
@pytest.mark.users
class TestUpdateUser:

    def test_put_user_returns_200(self, client: APIClient):
        assert_ok(client.put("/users/1", json=UserFactory.updated_payload()))

    def test_put_user_schema_is_valid(self, client: APIClient):
        assert_schema(client.put("/users/1", json=UserFactory.updated_payload()).json(), UPDATE_USER_RESPONSE)

    def test_put_user_returns_new_values(self, client: APIClient):
        payload = UserFactory.updated_payload()
        body = client.put("/users/1", json=payload).json()
        assert body["firstName"] == payload["firstName"]

    def test_patch_user_returns_200(self, client: APIClient):
        assert_ok(client.patch("/users/1", json=UserFactory.patch_payload()))


@pytest.mark.regression
@pytest.mark.users
class TestDeleteUser:

    def test_delete_user_returns_200(self, client: APIClient):
        assert_ok(client.delete("/users/1"))

    def test_delete_user_is_deleted_flag(self, client: APIClient):
        body = client.delete("/users/1").json()
        assert_schema(body, DELETE_USER_RESPONSE)
        assert body["isDeleted"] is True
