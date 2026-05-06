from typing import cast

import pytest
from datetime import date, datetime
from decimal import Decimal

from models.order import Order
from models.order_item import OrderItem


def test_create_valid_order():
    order = Order(
        customer_id=1,
        order_date=date(2026, 4, 20),
    )

    assert order.customer_id == 1
    assert order.order_date == date(2026, 4, 20)
    assert order.items == []
    assert order.order_id is None
    assert order.created_at is None
    assert order.updated_at is None
    assert order.deleted_at is None


def test_customer_id_must_be_greater_than_zero():
    with pytest.raises(ValueError, match="customer_id must be greater than zero"):
        Order(
            customer_id=0,
            order_date=date(2026, 4, 20),
        )


def test_customer_id_cannot_be_none():
    with pytest.raises(ValueError, match="customer_id must be greater than zero"):
        Order(
            customer_id=cast(int, None),
            order_date=date(2026, 4, 20),
        )


def test_order_date_is_required():
    with pytest.raises(ValueError, match="order_date is required"):
        Order(
            customer_id=1,
            order_date=cast(date, None),
        )


def test_items_starts_as_empty_list():
    order = Order(
        customer_id=1,
        order_date=date(2026, 4, 20),
    )

    assert isinstance(order.items, list)
    assert len(order.items) == 0


def test_add_item_appends_order_item():
    order = Order(
        customer_id=1,
        order_date=date(2026, 4, 20),
    )

    item = OrderItem(
        product_id=10,
        quantity=2,
        unit_price=Decimal("15.00"),
    )

    order.add_item(item)

    assert len(order.items) == 1
    assert order.items[0] is item


def test_add_item_rejects_invalid_type():
    order = Order(
        customer_id=1,
        order_date=date(2026, 4, 20),
    )

    with pytest.raises(TypeError, match="item must be an OrderItem"):
        order.add_item(cast(OrderItem, "not-an-order-item"))


def test_from_dict_creates_order_correctly():
    now = datetime.now()

    row = {
        "order_id": 5,
        "customer_id": 2,
        "order_date": date(2026, 4, 20),
        "created_at": now,
        "updated_at": now,
        "deleted_at": None,
    }

    order = Order.from_dict(row)

    assert order.order_id == 5
    assert order.customer_id == 2
    assert order.order_date == date(2026, 4, 20)
    assert order.items == []
    assert order.created_at == now
    assert order.updated_at == now
    assert order.deleted_at is None


def test_from_dict_missing_customer_id_raises_error():
    with pytest.raises(KeyError, match="customer_id"):
        Order.from_dict(
            {
                "order_date": date(2026, 4, 20),
            }
        )


def test_from_dict_missing_order_date_raises_error():
    with pytest.raises(KeyError, match="order_date"):
        Order.from_dict(
            {
                "customer_id": 1,
            }
        )


def test_to_dict_returns_expected_dictionary():
    now = datetime.now()

    order = Order(
        order_id=7,
        customer_id=3,
        order_date=date(2026, 4, 20),
        created_at=now,
        updated_at=now,
        deleted_at=None,
    )

    item = OrderItem(
        item_id=1,
        order_id=7,
        product_id=100,
        quantity=3,
        unit_price=Decimal("20.00"),
    )

    order.add_item(item)

    result = order.to_dict()

    assert result == {
        "order_id": 7,
        "customer_id": 3,
        "order_date": date(2026, 4, 20),
        "items": [
            {
                "item_id": 1,
                "order_id": 7,
                "product_id": 100,
                "quantity": 3,
                "unit_price": "20.00",
                "total": "60.00",
                "created_at": None,
                "updated_at": None,
                "deleted_at": None,
            }
        ],
        "created_at": now,
        "updated_at": now,
        "deleted_at": None,
    }
