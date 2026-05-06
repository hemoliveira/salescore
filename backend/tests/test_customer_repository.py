import pytest

from core.database import DatabaseManager
from models.customer import Customer
from repositories.customer_repository import CustomerRepository


def setup_module():
    DatabaseManager.init_pool()


def test_create_find_update_delete_customer():
    repo = CustomerRepository()

    customer = Customer(name="Teste Repository", city="SC")
    new_id = repo.create(customer)

    assert new_id > 0
    assert customer.customer_id == new_id

    found = repo.find_by_id(new_id)
    assert found is not None
    assert found.customer_id == new_id
    assert found.name == "Teste Repository"
    assert found.city == "SC"

    customer.city = "SP"
    updated = repo.update(customer)
    assert updated is True

    updated_customer = repo.find_by_id(new_id)
    assert updated_customer is not None
    assert updated_customer.city == "SP"

    deleted = repo.delete(new_id)
    assert deleted is True

    deleted_customer = repo.find_by_id(new_id)
    assert deleted_customer is None


def test_find_by_id_returns_none_when_customer_does_not_exist():
    repo = CustomerRepository()

    result = repo.find_by_id(999999999)

    assert result is None


def test_find_by_id_raises_error_for_invalid_id():
    repo = CustomerRepository()

    with pytest.raises(ValueError, match="customer_id must be greater than zero."):
        repo.find_by_id(0)


def test_update_returns_false_when_customer_does_not_exist():
    repo = CustomerRepository()

    customer = Customer(
        customer_id=999999999,
        name="Cliente Fantasma",
        city="Nowhere",
    )

    result = repo.update(customer)

    assert result is False


def test_update_raises_error_when_customer_id_is_invalid():
    repo = CustomerRepository()

    customer = Customer(
        customer_id=None,
        name="Sem ID",
        city="SC",
    )

    with pytest.raises(ValueError, match="customer_id is required."):
        repo.update(customer)


def test_delete_returns_false_when_customer_does_not_exist():
    repo = CustomerRepository()

    result = repo.delete(999999999)

    assert result is False


def test_delete_raises_error_for_invalid_id():
    repo = CustomerRepository()

    with pytest.raises(ValueError, match="customer_id must be greater than zero."):
        repo.delete(0)


def test_find_all_returns_customers_list():
    repo = CustomerRepository()

    customers = repo.find_all()

    assert isinstance(customers, list)

    for customer in customers:
        assert isinstance(customer, Customer)
