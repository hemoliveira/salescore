from typing import Optional

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: Optional[str] = Field(None, max_length=50)
    price: float = Field(..., ge=0)


class ProductUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: Optional[str] = Field(None, max_length=50)
    price: float = Field(..., ge=0)


class ProductResponse(BaseModel):
    product_id: int
    name: str
    category: Optional[str] = None
    price: float
