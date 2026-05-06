import pytest
from datetime import datetime
from decimal import Decimal

from models.product import Product


def test_create_valid_product():
    product = Product(
        name="Notebook",
        category="Electronics",
        price=Decimal("3500.00"),
    )

    assert product.name == "Notebook"
    assert product.category == "Electronics"
    assert product.price == Decimal("3500.00")
    assert product.product_id is None
    assert product.created_at is None
    assert product.updated_at is None
    assert product.deleted_at is None


def test_name_is_stripped():
    product = Product(
        name="  Mouse Gamer  ",
        category="Accessories",
        price=Decimal("100"),
    )

    assert product.name == "Mouse Gamer"


def test_name_cannot_be_empty():
    with pytest.raises(ValueError, match="name cannot be empty"):
        Product(name="   ", price=Decimal("10"))


def test_name_cannot_exceed_100_characters():
    with pytest.raises(ValueError, match="name must have at most 100 characters"):
        Product(name="a" * 101, price=Decimal("10"))


def test_category_is_stripped():
    product = Product(
        name="Keyboard",
        category="  Peripherals  ",
        price=Decimal("200"),
    )

    assert product.category == "Peripherals"


def test_category_empty_becomes_none():
    product = Product(
        name="Keyboard",
        category="   ",
        price=Decimal("200"),
    )

    assert product.category is None


def test_category_can_be_none():
    product = Product(
        name="Keyboard",
        category=None,
        price=Decimal("200"),
    )

    assert product.category is None


def test_category_cannot_exceed_50_characters():
    with pytest.raises(ValueError, match="category must have at most 50 characters"):
        Product(
            name="Keyboard",
            category="a" * 51,
            price=Decimal("200"),
        )


def test_price_is_converted_to_decimal():
    product = Product(
        name="Monitor",
        category="Electronics",
        price=Decimal("1500"),
    )

    assert isinstance(product.price, Decimal)
    assert product.price == Decimal("1500")


def test_price_can_be_zero():
    product = Product(
        name="Free Item",
        price=Decimal("0"),
    )

    assert product.price == Decimal("0")


def test_price_cannot_be_negative():
    with pytest.raises(ValueError, match="price cannot be negative"):
        Product(
            name="Invalid Product",
            price=Decimal("-10"),
        )


def test_from_dict_creates_product_correctly():
    now = datetime.now()

    row = {
        "product_id": 1,
        "name": "Headset",
        "category": "Audio",
        "price": "299.90",
        "created_at": now,
        "updated_at": now,
        "deleted_at": None,
    }

    product = Product.from_dict(row)

    assert product.product_id == 1
    assert product.name == "Headset"
    assert product.category == "Audio"
    assert product.price == Decimal("299.90")
    assert product.created_at == now
    assert product.updated_at == now
    assert product.deleted_at is None


def test_from_dict_missing_name_raises_error():
    with pytest.raises(KeyError, match="name"):
        Product.from_dict({"price": 10})


def test_from_dict_missing_price_uses_zero():
    with pytest.raises(KeyError, match="price"):
        Product.from_dict({"name": "Gift"})


def test_to_dict_returns_expected_dictionary():
    now = datetime.now()

    product = Product(
        product_id=10,
        name="Webcam",
        category="Video",
        price=Decimal("450.50"),
        created_at=now,
        updated_at=now,
        deleted_at=None,
    )

    result = product.to_dict()

    assert result == {
        "product_id": 10,
        "name": "Webcam",
        "category": "Video",
        "price": "450.50",
        "created_at": now,
        "updated_at": now,
        "deleted_at": None,
    }
