from datetime import date
from typing import List

from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class OrderItemResponse(BaseModel):
    item_id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: str
    total: str


class OrderCreate(BaseModel):
    customer_id: int = Field(..., gt=0)
    order_date: date
    items: List[OrderItemCreate] = Field(..., min_length=1)


class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    order_date: date
    items: List[OrderItemResponse]
