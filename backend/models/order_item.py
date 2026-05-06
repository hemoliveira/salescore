from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any


@dataclass(slots=True, kw_only=True)
class OrderItem:
    product_id: int
    quantity: int
    unit_price: Decimal

    item_id: int | None = None
    order_id: int | None = None
    total: Decimal = Decimal("0.00")

    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.product_id <= 0:
            raise ValueError("product_id must be greater than zero")

        if self.quantity <= 0:
            raise ValueError("quantity must be greater than zero")

        if not isinstance(self.unit_price, Decimal):
            self.unit_price = Decimal(str(self.unit_price))

        if not isinstance(self.total, Decimal):
            self.total = Decimal(str(self.total))

        if self.unit_price < Decimal("0"):
            raise ValueError("unit_price cannot be negative")

        if self.item_id is not None and self.item_id <= 0:
            raise ValueError("item_id must be greater than zero")

        if self.order_id is not None and self.order_id <= 0:
            raise ValueError("order_id must be greater than zero")

        self.total = self.unit_price * self.quantity

    @classmethod
    def from_dict(cls, row: dict[str, Any]) -> "OrderItem":
        return cls(
            item_id=row.get("item_id"),
            order_id=row.get("order_id"),
            product_id=row["product_id"],
            quantity=row.get("quantity", 1),
            unit_price=row.get("unit_price", 0),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
            deleted_at=row.get("deleted_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": str(self.unit_price),
            "total": str(self.total),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }
