"""
Tests for /products endpoint — DummyJSON.
"""
import pytest
from src.api_client import APIClient
from src.schemas.api_schemas import PRODUCT_LIST_RESPONSE, PRODUCT_OBJECT
from src.utils.assertions import (
    assert_ok, assert_not_found, assert_schema,
    assert_response_time, assert_list_not_empty,
)


@pytest.mark.smoke
@pytest.mark.resources
class TestGetProducts:

    def test_list_products_returns_200(self, client: APIClient):
        assert_ok(client.get("/products"))

    def test_list_products_schema_is_valid(self, client: APIClient):
        assert_schema(client.get("/products").json(), PRODUCT_LIST_RESPONSE)

    def test_list_products_contains_items(self, client: APIClient):
        assert_list_not_empty(client.get("/products").json()["products"])

    def test_list_products_limit_param(self, client: APIClient):
        body = client.get("/products", params={"limit": 5}).json()
        assert len(body["products"]) <= 5

    @pytest.mark.performance
    def test_list_products_response_time(self, client: APIClient):
        assert_response_time(client.get("/products"))


@pytest.mark.smoke
@pytest.mark.resources
class TestGetSingleProduct:

    def test_get_product_returns_200(self, client: APIClient):
        assert_ok(client.get("/products/1"))

    def test_get_product_schema_is_valid(self, client: APIClient):
        assert_schema(client.get("/products/1").json(), PRODUCT_OBJECT)

    def test_get_product_price_is_positive(self, client: APIClient):
        price = client.get("/products/1").json()["price"]
        assert price > 0

    def test_get_product_returns_correct_id(self, client: APIClient):
        assert client.get("/products/2").json()["id"] == 2

    @pytest.mark.negative
    def test_get_nonexistent_product_returns_404(self, client: APIClient):
        assert_not_found(client.get("/products/99999"))
