from tests.test_utils import unique_text


def test_create_get_update_delete_product(client):
    unique_name = unique_text("Produto API")

    # CREATE
    response = client.post(
        "/products",
        json={
            "name": unique_name,
            "category": "Electronics",
            "price": 199.90,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Product created successfully"
    product_id = data["product_id"]
    assert product_id > 0

    # GET BY ID
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["product_id"] == product_id
    assert data["name"] == unique_name
    assert data["category"] == "Electronics"
    assert data["price"] == 199.9

    # UPDATE
    updated_name = unique_text("Produto API Atualizado")

    response = client.put(
        f"/products/{product_id}",
        json={
            "name": updated_name,
            "category": "Updated Category",
            "price": 249.90,
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Product updated successfully"

    # DELETE
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Product deleted successfully"

    # GET AFTER DELETE
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_create_product_invalid_price(client):
    response = client.post(
        "/products",
        json={
            "name": unique_text("Produto Inválido"),
            "category": "Test",
            "price": -10,
        },
    )

    assert response.status_code == 422


def test_get_created_product(client, created_product):
    product_id = created_product["product_id"]

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == product_id
