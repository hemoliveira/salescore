import pytest
import uuid
from decimal import Decimal

from core.database import DatabaseManager
from models.product import Product
from repositories.product_repository import ProductRepository


def setup_module():
    DatabaseManager.init_pool()


def test_create_find_update_delete_product():
    repo = ProductRepository()

    unique_name = f"Produto Repository {uuid.uuid4().hex[:8]}"

    # CREATE
    product = Product(
        name=unique_name,
        category="Test Category",
        price=Decimal("99.90"),
    )
    new_id = repo.create(product)

    assert new_id > 0
    assert product.product_id == new_id

    # FIND BY ID
    found = repo.find_by_id(new_id)
    assert found is not None
    assert found.product_id == new_id
    assert found.name == unique_name
    assert found.category == "Test Category"
    assert found.price == product.price

    # UPDATE
    updated_name = f"Produto Atualizado {uuid.uuid4().hex[:8]}"
    product.name = updated_name
    product.category = "Updated Category"
    product.price = product.price + Decimal("10.00")

    updated = repo.update(product)
    assert updated is True

    updated_product = repo.find_by_id(new_id)
    assert updated_product is not None
    assert updated_product.name == updated_name
    assert updated_product.category == "Updated Category"
    assert updated_product.price == product.price

    # DELETE (soft delete)
    deleted = repo.delete(new_id)
    assert deleted is True

    deleted_product = repo.find_by_id(new_id)
    assert deleted_product is None


def test_find_by_id_returns_none_when_product_does_not_exist():
    repo = ProductRepository()

    result = repo.find_by_id(999999999)

    assert result is None


def test_find_by_id_raises_error_for_invalid_id():
    repo = ProductRepository()

    with pytest.raises(ValueError, match="product_id must be greater than zero."):
        repo.find_by_id(0)


def test_update_returns_false_when_product_does_not_exist():
    repo = ProductRepository()

    product = Product(
        product_id=999999999,
        name="Produto Fantasma",
        category="Nowhere",
        price=Decimal("10.00"),
    )

    result = repo.update(product)

    assert result is False


def test_update_raises_error_when_product_id_is_invalid():
    repo = ProductRepository()

    product = Product(
        product_id=None,
        name="Sem ID",
        category="SC",
        price=Decimal("10.00"),
    )

    with pytest.raises(ValueError, match="product_id is required."):
        repo.update(product)


def test_delete_returns_false_when_product_does_not_exist():
    repo = ProductRepository()

    result = repo.delete(999999999)

    assert result is False


def test_delete_raises_error_for_invalid_id():
    repo = ProductRepository()

    with pytest.raises(ValueError, match="product_id must be greater than zero."):
        repo.delete(0)


def test_find_all_returns_products_list():
    repo = ProductRepository()

    products = repo.find_all()

    assert isinstance(products, list)

    for product in products:
        assert isinstance(product, Product)
