from pydantic import BaseModel
from typing import Optional
class ProductCreate(BaseModel):
    name: str
    unit: str
    category: str
    cost: float
    price: float

    # Para actualizar un producto (todos los campos opcionales)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    unit: Optional[str] = None
    category: Optional[str] = None
    cost: Optional[float] = None
    price: Optional[float] = None

# Opcional: schema para respuesta con ID
class ProductResponse(BaseModel):
    id: int
    name: str
    unit: str
    category: str
    cost: float
    price: float
    activo: bool = True

    class Config:
        orm_mode = True