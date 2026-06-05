from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

import database_models
from database_models import Products
from database import SessionLocal, engine


# ------------------ DB SESSION ------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------ APP ------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://fast-a-pi-practice.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)


# ------------------ SCHEMA (IMPORTANT FIX) ------------------

class ProductSchema(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

    class Config:
        from_attributes = True


# ------------------ ROUTES ------------------

@app.get("/")
def greet():
    return {"message": "Welcome to FastAPI!"}


# ✅ CREATE
@app.post("/products")
def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    new_product = Products(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# ✅ READ ALL
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Products).all()


# ✅ READ ONE
@app.get("/products/{product_id}")
def get_single_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == product_id).first()

    if not product:
        return {"error": "Product not found"}

    return product


# ✅ UPDATE
@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: ProductSchema, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == product_id).first()

    if not product:
        return {"error": "Product not found"}

    product.name = updated_product.name
    product.description = updated_product.description
    product.price = updated_product.price
    product.quantity = updated_product.quantity

    db.commit()
    return {"message": "Product updated successfully"}


# ✅ DELETE
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == product_id).first()

    if not product:
        return {"error": "Product not found"}

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}