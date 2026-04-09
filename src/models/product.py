from sqlalchemy import Column, Integer, String, Float, Boolean
from src.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    unidad = Column(String)
    categoria = Column(String)
    costo = Column(Float)
    precio = Column(Float)
    activo = Column(Boolean, default=True)