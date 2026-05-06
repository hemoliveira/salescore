import pytest
from datetime import datetime
from decimal import Decimal

from models.order_item import OrderItem


def test_create_valid_order_item():
    item = OrderItem(
        product_id=1,
        quantity=2,
        unit_price=Decimal("10.50"),
    )

    assert item.product_id == 1
    assert item.quantity == 2
    assert item.unit_price == Decimal("10.50")
    assert item.total == Decimal("21.00")
    assert item.order_id is None
    assert item.item_id is None
    assert item.created_at is None
    assert item.updated_at is None
    assert item.deleted_at is None


def test_product_id_must_be_greater_than_zero():
    with pytest.raises(ValueError, match="product_id must be greater than zero"):
        OrderItem(
            product_id=0,
            quantity=1,
            unit_price=Decimal("10"),
        )


def test_quantity_must_be_greater_than_zero():
    with pytest.raises(ValueError, match="quantity must be greater than zero"):
        OrderItem(
            product_id=1,
            quantity=0,
            unit_price=Decimal("10"),
        )


def test_unit_price_is_converted_to_decimal():
    item = OrderItem(
        product_id=1,
        quantity=3,
        unit_price=Decimal("10"),
    )

    assert isinstance(item.unit_price, Decimal)
    assert item.unit_price == Decimal("10")
    assert item.total == Decimal("30")


def test_total_is_converted_and_recalculated():
    item = OrderItem(
        product_id=1,
        quantity=2,
        unit_price=Decimal("15.00"),
        total=Decimal("999.99"),
    )

    assert isinstance(item.unit_price, Decimal)
    assert isinstance(item.total, Decimal)
    assert item.unit_price == Decimal("15.00")
    assert item.total == Decimal("30.00")


def test_unit_price_cannot_be_negative():
    with pytest.raises(ValueError, match="unit_price cannot be negative"):
        OrderItem(
            product_id=1,
            quantity=2,
            unit_price=Decimal("-1"),
        )


def test_unit_price_can_be_zero():
    item = OrderItem(
        product_id=1,
        quantity=2,
        unit_price=Decimal("0"),
    )

    assert item.unit_price == Decimal("0")
    assert item.total == Decimal("0")


def test_from_dict_creates_order_item_correctly():
    now = datetime.now()

    row = {
        "item_id": 10,
        "order_id": 20,
        "product_id": 3,
        "quantity": 4,
        "unit_price": "12.50",
        "total": "999.99",  # será recalculado
        "created_at": now,
        "updated_at": now,
        "deleted_at": None,
    }

    item = OrderItem.from_dict(row)

    assert item.item_id == 10
    assert item.order_id == 20
    assert item.product_id == 3
    assert item.quantity == 4
    assert item.unit_price == Decimal("12.50")
    assert item.total == Decimal("50.00")
    assert item.created_at == now
    assert item.updated_at == now
    assert item.deleted_at is None


def test_from_dict_missing_quantity_uses_default_one():
    item = OrderItem.from_dict(
        {
            "product_id": 2,
            "unit_price": "7.00",
        }
    )

    assert item.quantity == 1
    assert item.unit_price == Decimal("7.00")
    assert item.total == Decimal("7.00")


def test_to_dict_returns_expected_dictionary():
    now = datetime.now()

    item = OrderItem(
        item_id=1,
        order_id=2,
        product_id=3,
        quantity=5,
        unit_price=Decimal("8.40"),
        created_at=now,
        updated_at=now,
        deleted_at=None,
    )

    result = item.to_dict()

    assert result == {
        "item_id": 1,
        "order_id": 2,
        "product_id": 3,
        "quantity": 5,
        "unit_price": "8.40",
        "total": "42.00",
        "created_at": now,
        "updated_at": now,
        "deleted_at": None,
    }
