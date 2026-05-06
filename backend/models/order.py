from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

from models.order_item import OrderItem


@dataclass(slots=True, kw_only=True)
class Order:
    customer_id: int
    order_date: date
    items: list[OrderItem] = field(default_factory=list)
    order_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.customer_id is None or self.customer_id <= 0:
            raise ValueError("customer_id must be greater than zero")

        if self.order_date is None:
            raise ValueError("order_date is required")

        if not isinstance(self.order_date, date):
            raise TypeError("order_date must be a date")

        if self.order_id is not None and self.order_id <= 0:
            raise ValueError("order_id must be greater than zero")

    @classmethod
    def from_dict(cls, row: dict[str, Any]) -> "Order":
        return cls(
            order_id=row.get("order_id"),
            customer_id=row["customer_id"],
            order_date=row["order_date"],
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
            deleted_at=row.get("deleted_at"),
        )

    def add_item(self, item: OrderItem) -> None:
        if not isinstance(item, OrderItem):
            raise TypeError("item must be an OrderItem")
        self.items.append(item)

    def to_dict(self) -> dict[str, Any]:
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "order_date": self.order_date,
            "items": [item.to_dict() for item in self.items],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }
