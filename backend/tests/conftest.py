import uuid
import pytest
from fastapi.testclient import TestClient
from tests.test_utils import unique_text

from main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def created_customer(client):
    response = client.post(
        "/customers",
        json={
            "name": unique_text("Cliente Fixture"),
            "city": "Florianópolis",
        },
    )

    assert response.status_code == 201
    return response.json()


@pytest.fixture
def created_product(client):
    response = client.post(
        "/products",
        json={
            "name": unique_text("Produto Fixture"),
            "category": "Category Fixture",
            "price": 99.90,
        },
    )

    assert response.status_code == 201
    return response.json()


@pytest.fixture
def created_order(client, created_customer):
    product1_response = client.post(
        "/products",
        json={
            "name": unique_text("Produto Order Fixture 1"),
            "category": "Category A",
            "price": 10.00,
        },
    )
    assert product1_response.status_code == 201
    product1_id = product1_response.json()["product_id"]

    product2_response = client.post(
        "/products",
        json={
            "name": unique_text("Produto Order Fixture 2"),
            "category": "Category B",
            "price": 20.00,
        },
    )
    assert product2_response.status_code == 201
    product2_id = product2_response.json()["product_id"]

    response = client.post(
        "/orders",
        json={
            "customer_id": created_customer["customer_id"],
            "order_date": "2026-04-20",
            "items": [
                {"product_id": product1_id, "quantity": 2},
                {"product_id": product2_id, "quantity": 1},
            ],
        },
    )

    assert response.status_code == 201
    return response.json()
