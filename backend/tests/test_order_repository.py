import pytest
from datetime import date
from decimal import Decimal
import uuid

from core.database import DatabaseManager
from models.customer import Customer
from models.product import Product
from models.order import Order
from models.order_item import OrderItem

from repositories.customer_repository import CustomerRepository
from repositories.product_repository import ProductRepository
from repositories.order_repository import OrderRepository


def setup_module():
    DatabaseManager.init_pool()


def unique_text(prefix: str) -> str:
    return f"{prefix} {uuid.uuid4().hex[:8]}"


def test_create_find_delete_order():
    customer_repo = CustomerRepository()
    product_repo = ProductRepository()
    order_repo = OrderRepository()

    # customer
    customer = Customer(
        name=unique_text("Cliente Pedido"),
        city="SC",
    )
    customer_repo.create(customer)
    assert customer.customer_id is not None

    # products
    product1 = Product(
        name=unique_text("Produto 1"),
        category="Cat",
        price=Decimal("10.00"),
    )
    product_repo.create(product1)
    assert product1.product_id is not None

    product2 = Product(
        name=unique_text("Produto 2"),
        category="Cat",
        price=Decimal("20.00"),
    )
    product_repo.create(product2)
    assert product2.product_id is not None

    # order
    order = Order(
        customer_id=customer.customer_id,
        order_date=date.today(),
    )

    order.add_item(
        OrderItem(
            product_id=product1.product_id,
            quantity=2,
            unit_price=Decimal("0"),
        )
    )

    order.add_item(
        OrderItem(
            product_id=product2.product_id,
            quantity=1,
            unit_price=Decimal("0"),
        )
    )

    new_id = order_repo.create(order)

    assert new_id > 0
    assert order.order_id == new_id

    found = order_repo.find_by_id(new_id)

    assert found is not None
    assert found.order_id == new_id
    assert found.customer_id == customer.customer_id
    assert len(found.items) == 2

    # item totals
    assert found.items[0].total > 0
    assert found.items[1].total > 0

    # delete
    deleted = order_repo.delete(new_id)
    assert deleted is True

    deleted_order = order_repo.find_by_id(new_id)
    assert deleted_order is None


def test_create_order_without_items_raises_error():
    repo = OrderRepository()

    order = Order(
        customer_id=1,
        order_date=date.today(),
    )

    with pytest.raises(ValueError, match="Order must contain at least one item"):
        repo.create(order)


def test_create_order_with_invalid_customer():
    repo = OrderRepository()

    order = Order(
        customer_id=999999999,
        order_date=date.today(),
    )

    order.add_item(OrderItem(product_id=1, quantity=1, unit_price=Decimal("0")))

    with pytest.raises(ValueError):
        repo.create(order)


def test_update_order_success(created_customer):
    repo = OrderRepository()
    order = Order(
        customer_id=created_customer["customer_id"],
        order_date=date(2026, 4, 20),
        items=[
            OrderItem(
                product_id=1,
                quantity=1,
                unit_price=Decimal("10.00"),
            )
        ],
    )

    order_id = repo.create(order)

    order.order_id = order_id
    order.order_date = date(2026, 4, 21)

    updated = repo.update(order)

    assert updated is True

    found_order = repo.find_by_id(order_id)

    assert found_order is not None
    assert found_order.order_date == date(2026, 4, 21)


def test_update_order_returns_false_when_order_not_found(created_customer):
    order_repository = OrderRepository()
    order = Order(
        order_id=999999,
        customer_id=created_customer["customer_id"],
        order_date=date(2026, 4, 20),
    )

    updated = order_repository.update(order)

    assert updated is False


def test_add_item_success(created_customer):
    order_repository = OrderRepository()
    order = Order(
        customer_id=created_customer["customer_id"],
        order_date=date(2026, 4, 20),
        items=[
            OrderItem(
                product_id=1,
                quantity=1,
                unit_price=Decimal("10.00"),
            )
        ],
    )

    order_id = order_repository.create(order)

    new_item = OrderItem(
        product_id=1,
        quantity=2,
        unit_price=Decimal("0.00"),
    )

    item_id = order_repository.add_item(order_id, new_item)

    assert item_id > 0
    assert new_item.item_id == item_id
    assert new_item.order_id == order_id
    assert new_item.total == new_item.unit_price * new_item.quantity

    found_order = order_repository.find_by_id(order_id)

    assert found_order is not None
    assert len(found_order.items) == 2


def test_add_item_rejects_invalid_order_id():
    order_repository = OrderRepository()
    item = OrderItem(
        product_id=1,
        quantity=1,
        unit_price=Decimal("10.00"),
    )

    try:
        order_repository.add_item(0, item)
        assert False
    except ValueError as exc:
        assert str(exc) == "order_id must be greater than zero."


def test_remove_item_success(created_customer):
    order_repository = OrderRepository()
    order = Order(
        customer_id=created_customer["customer_id"],
        order_date=date(2026, 4, 20),
        items=[
            OrderItem(
                product_id=1,
                quantity=1,
                unit_price=Decimal("10.00"),
            )
        ],
    )

    order_id = order_repository.create(order)

    found_order = order_repository.find_by_id(order_id)

    assert found_order is not None
    assert len(found_order.items) == 1

    item_id = found_order.items[0].item_id

    assert item_id is not None

    removed = order_repository.remove_item(order_id, item_id)

    assert removed is True

    found_order_after_remove = order_repository.find_by_id(order_id)

    assert found_order_after_remove is not None
    assert len(found_order_after_remove.items) == 0


def test_remove_item_returns_false_when_item_not_found(created_customer):
    order_repository = OrderRepository()
    order = Order(
        customer_id=created_customer["customer_id"],
        order_date=date(2026, 4, 20),
        items=[
            OrderItem(
                product_id=1,
                quantity=1,
                unit_price=Decimal("10.00"),
            )
        ],
    )

    order_id = order_repository.create(order)

    removed = order_repository.remove_item(order_id, 999999)

    assert removed is False
