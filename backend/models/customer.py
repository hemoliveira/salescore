from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True, kw_only=True)
class Customer:
    name: str
    city: str | None = None
    customer_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    def __post_init__(self) -> None:
        self.name = self.name.strip()

        if not self.name:
            raise ValueError("name cannot be empty")

        if len(self.name) > 100:
            raise ValueError("name must have at most 100 characters")

        if self.city is not None:
            self.city = self.city.strip() or None

            if self.city is not None and len(self.city) > 50:
                raise ValueError("city must have at most 50 characters")

    @classmethod
    def from_dict(cls, row: dict[str, Any]) -> "Customer":
        return cls(
            customer_id=row.get("customer_id"),
            name=row["name"],
            city=row.get("city"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
            deleted_at=row.get("deleted_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "city": self.city,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }
