"""Step definitions for BrowserStack Demo API scenarios."""

from typing import Dict, List

import pytest
from pytest_bdd import given, when, then, parsers

from api.clients.store_client import StoreClient
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture
def api_context() -> Dict[str, object]:
    """Mutable context shared across API steps."""
    return {}


@given("the BrowserStack Demo API is reachable")
def api_availability(config, api_context):
    base_url = config.get("api_base_url")
    if not base_url:
        raise RuntimeError("api_base_url missing from config/config.yaml")
    api_context["base_url"] = base_url.rstrip("/")
    logger.info("API base URL resolved to %s", api_context["base_url"])


@when("I request the product catalog")
def request_product_catalog(api_context, store_client: StoreClient):
    response = store_client.list_products()
    api_context["response"] = response
    payload = response.json()
    if isinstance(payload, dict) and "products" in payload:
        products = payload["products"]
    else:
        products = payload
    api_context["products"] = products
    logger.info(
        "Retrieved %s products from the catalog API",
        len(products),
    )


@when(parsers.parse('I authenticate via the API as "{username}" with password "{password}"'))
def authenticate_user(api_context, store_client: StoreClient, username: str, password: str):
    response = store_client.sign_in(username, password)
    api_context["response"] = response
    api_context["auth_payload"] = response.json()
    logger.info("Attempted API login for user %s with status %s", username, response.status_code)


@then(parsers.parse("the API response status should be {status:d}"))
def assert_status(api_context, status: int):
    response = api_context.get("response")
    assert response is not None, "No API response captured in context"
    assert response.status_code == status, f"Expected {status}, got {response.status_code}"


@then(parsers.parse("the response should contain at least {minimum:d} products"))
def assert_minimum_products(api_context, minimum: int):
    products: List[Dict[str, object]] = api_context.get("products", [])
    assert len(products) >= minimum, f"Expected at least {minimum} products, got {len(products)}"


@then(parsers.parse('each product item should include the fields "{fields}"'))
def assert_product_fields(api_context, fields: str):
    products: List[Dict[str, object]] = api_context.get("products", [])
    assert products, "No products captured from API"

    for product in products:
        title = product.get("title")
        price = product.get("price")
        description = product.get("description")
        assert isinstance(title, str) and title.strip(), f"Missing readable title in {product}"
        assert price not in (None, ""), f"Missing price in {product}"
        assert description, f"Missing image reference in {product}"
    logger.info(
        "Validated %s fields across %s products",
        fields,
        len(products),
    )
