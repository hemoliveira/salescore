from tests.test_utils import unique_text


def test_create_get_delete_order(client):
    # CREATE CUSTOMER
    customer_response = client.post(
        "/customers",
        json={
            "name": unique_text("Cliente Pedido API"),
            "city": "Florianópolis",
        },
    )
    assert customer_response.status_code == 201
    customer_id = customer_response.json()["customer_id"]

    # CREATE PRODUCTS
    product1_response = client.post(
        "/products",
        json={
            "name": unique_text("Produto Pedido API 1"),
            "category": "Category A",
            "price": 10.00,
        },
    )
    assert product1_response.status_code == 201
    product1_id = product1_response.json()["product_id"]

    product2_response = client.post(
        "/products",
        json={
            "name": unique_text("Produto Pedido API 2"),
            "category": "Category B",
            "price": 20.00,
        },
    )
    assert product2_response.status_code == 201
    product2_id = product2_response.json()["product_id"]

    # CREATE ORDER
    response = client.post(
        "/orders",
        json={
            "customer_id": customer_id,
            "order_date": "2026-04-20",
            "items": [
                {"product_id": product1_id, "quantity": 2},
                {"product_id": product2_id, "quantity": 1},
            ],
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Order created successfully"
    order_id = data["order_id"]
    assert order_id > 0

    # GET BY ID
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["order_id"] == order_id
    assert data["customer_id"] == customer_id
    assert len(data["items"]) == 2

    # DELETE
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Order deleted successfully"

    # GET AFTER DELETE
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


def test_create_order_without_items(client):
    customer_response = client.post(
        "/customers",
        json={
            "name": unique_text("Cliente Sem Itens API"),
            "city": "SC",
        },
    )
    assert customer_response.status_code == 201
    customer_id = customer_response.json()["customer_id"]

    response = client.post(
        "/orders",
        json={
            "customer_id": customer_id,
            "order_date": "2026-04-20",
            "items": [],
        },
    )

    assert response.status_code == 422


def test_create_get_delete_order_with_customer(client, created_order, created_customer):
    order_id = created_order["order_id"]

    # GET BY ID
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["order_id"] == order_id
    assert data["customer_id"] == created_customer["customer_id"]
    assert len(data["items"]) == 2

    # DELETE
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Order deleted successfully"

    # GET AFTER DELETE
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


def test_create_order_without_items_with_customer(client, created_customer):
    response = client.post(
        "/orders",
        json={
            "customer_id": created_customer["customer_id"],
            "order_date": "2026-04-20",
            "items": [],
        },
    )

    assert response.status_code == 422
