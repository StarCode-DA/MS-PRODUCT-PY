from pydantic import BaseModel, validator
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    unit: str
    category: str
    cost: float
    price: float

    @validator("price")
    def price_must_be_greater_than_cost(cls, price, values):
        cost = values.get("cost")
        if cost is not None and price <= cost:
            raise ValueError("Sale price must be greater than cost")
        return price

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    unit: Optional[str] = None
    category: Optional[str] = None
    cost: Optional[float] = None
    price: Optional[float] = None

    @validator("price", always=True)
    def price_must_be_greater_than_cost(cls, price, values):
        cost = values.get("cost")
        if price is not None and cost is not None and price <= cost:
            raise ValueError("Sale price must be greater than cost")
        return price

class ProductResponse(BaseModel):
    id: int
    name: str
    unit: str
    category: str
    cost: float
    price: float
    activo: bool = True

    model_config = {"from_attributes": True}