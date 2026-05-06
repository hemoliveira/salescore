import pytest
from datetime import datetime

from models.customer import Customer


def test_create_valid_customer():
    customer = Customer(name="Henrique", city="Florianópolis")

    assert customer.name == "Henrique"
    assert customer.city == "Florianópolis"
    assert customer.customer_id is None
    assert customer.created_at is None
    assert customer.updated_at is None
    assert customer.deleted_at is None


def test_name_is_stripped():
    customer = Customer(name="  Henrique  ", city="SC")

    assert customer.name == "Henrique"


def test_name_cannot_be_empty():
    with pytest.raises(ValueError, match="name cannot be empty"):
        Customer(name="   ")


def test_name_cannot_exceed_100_characters():
    with pytest.raises(ValueError, match="name must have at most 100 characters"):
        Customer(name="a" * 101)


def test_city_is_stripped():
    customer = Customer(name="Henrique", city="  São Paulo  ")

    assert customer.city == "São Paulo"


def test_city_empty_becomes_none():
    customer = Customer(name="Henrique", city="   ")

    assert customer.city is None


def test_city_can_be_none():
    customer = Customer(name="Henrique", city=None)

    assert customer.city is None


def test_city_cannot_exceed_50_characters():
    with pytest.raises(ValueError, match="city must have at most 50 characters"):
        Customer(name="Henrique", city="a" * 51)


def test_from_dict_creates_customer_correctly():
    now = datetime.now()

    row = {
        "customer_id": 1,
        "name": "Maria",
        "city": "Curitiba",
        "created_at": now,
        "updated_at": now,
        "deleted_at": None,
    }

    customer = Customer.from_dict(row)

    assert customer.customer_id == 1
    assert customer.name == "Maria"
    assert customer.city == "Curitiba"
    assert customer.created_at == now
    assert customer.updated_at == now
    assert customer.deleted_at is None


def test_from_dict_uses_empty_name_when_missing():
    with pytest.raises(KeyError, match="name"):
        Customer.from_dict({})


def test_to_dict_returns_expected_dictionary():
    now = datetime.now()

    customer = Customer(
        customer_id=10,
        name="João",
        city="Porto Alegre",
        created_at=now,
        updated_at=now,
        deleted_at=None,
    )

    result = customer.to_dict()

    assert result == {
        "customer_id": 10,
        "name": "João",
        "city": "Porto Alegre",
        "created_at": now,
        "updated_at": now,
        "deleted_at": None,
    }
