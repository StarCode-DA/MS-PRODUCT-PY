from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models.product import Product
from src.schemas.product import ProductCreate, ProductUpdate

router = APIRouter(prefix="/productos/product", tags=["Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET
@router.get("/")
def get_products(name: str = None, category: str = None, db: Session = Depends(get_db)):
    query = db.query(Product)

    if name:
        query = query.filter(Product.nombre.ilike(f"%{name}%"))

    if category:
        query = query.filter(Product.categoria == category)

    products = query.order_by(Product.id).all()

    return [
        {
            "id": p.id,
            "name": p.nombre,
            "unit": p.unidad,
            "category": p.categoria,
            "cost": p.costo,
            "price": p.precio,
            "activo": p.activo
        }
        for p in products
    ]

# CREATE
@router.post("/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        nombre=product.name,
        unidad=product.unit,
        categoria=product.category,
        costo=product.cost,
        precio=product.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "id": new_product.id,
        "name": new_product.nombre,
        "unit": new_product.unidad,
        "category": new_product.categoria,
        "cost": new_product.costo,
        "price": new_product.precio,
        "activo": new_product.activo
    }

# UPDATE
@router.put("/{id}")
def update_product(id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == id).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.nombre = product.name
    db_product.unidad = product.unit
    db_product.categoria = product.category
    db_product.costo = product.cost
    db_product.precio = product.price

    db.commit()
    db.refresh(db_product)

    return {
        "id": db_product.id,
        "name": db_product.nombre,
        "unit": db_product.unidad,
        "category": db_product.categoria,
        "cost": db_product.costo,
        "price": db_product.precio,
        "activo": db_product.activo
    }
    
    # TOGGLE ACTIVO
@router.patch("/{id}/toggle-activo")
def toggle_activo(id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == id).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.activo = not db_product.activo
    db.commit()
    db.refresh(db_product)

    return {
        "id": db_product.id,
        "name": db_product.nombre,
        "activo": db_product.activo
    }