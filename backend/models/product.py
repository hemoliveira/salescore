from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any


@dataclass(slots=True, kw_only=True)
class Product:
    name: str
    price: Decimal
    category: str | None = None
    product_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    def __post_init__(self) -> None:
        self.name = self.name.strip()

        if not self.name:
            raise ValueError("name cannot be empty")

        if len(self.name) > 100:
            raise ValueError("name must have at most 100 characters")

        if self.category is not None:
            self.category = self.category.strip() or None

            if self.category is not None and len(self.category) > 50:
                raise ValueError("category must have at most 50 characters")

        if not isinstance(self.price, Decimal):
            self.price = Decimal(str(self.price))

        if self.price < Decimal("0"):
            raise ValueError("price cannot be negative")

    @classmethod
    def from_dict(cls, row: dict[str, Any]) -> "Product":
        return cls(
            product_id=row.get("product_id"),
            name=row["name"],
            price=row["price"],
            category=row.get("category"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
            deleted_at=row.get("deleted_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": str(self.price),
            "category": self.category,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }
