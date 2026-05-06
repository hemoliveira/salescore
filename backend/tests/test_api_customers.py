from tests.test_utils import unique_text


def test_create_get_update_delete_customer(client):
    unique_name = unique_text("Cliente API")

    # CREATE
    response = client.post(
        "/customers",
        json={
            "name": unique_name,
            "city": "Florianópolis",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Customer created successfully"

    customer_id = data["customer_id"]
    assert customer_id > 0

    # GET BY ID
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["customer_id"] == customer_id
    assert data["name"] == unique_name
    assert data["city"] == "Florianópolis"

    # UPDATE
    updated_name = unique_text("Cliente API Atualizado")

    response = client.put(
        f"/customers/{customer_id}",
        json={
            "name": updated_name,
            "city": "São Paulo",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Customer updated successfully"

    # DELETE
    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Customer deleted successfully"

    # GET AFTER DELETE
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"


def test_create_customer_invalid_payload(client):
    response = client.post(
        "/customers",
        json={
            "name": "",
            "city": "SC",
        },
    )

    assert response.status_code == 422


def test_get_created_customer(client, created_customer):
    customer_id = created_customer["customer_id"]

    response = client.get(f"/customers/{customer_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == customer_id
