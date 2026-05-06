from typing import Optional

from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    city: Optional[str] = Field(None, max_length=50)


class CustomerUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    city: Optional[str] = Field(None, max_length=50)


class CustomerResponse(BaseModel):
    customer_id: int
    name: str
    city: Optional[str] = None
