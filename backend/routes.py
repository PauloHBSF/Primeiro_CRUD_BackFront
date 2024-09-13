from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal, get_db
from schemas import ProductRead, ProductUpdate, ProductCreate
from crud import (
    create_product,
    get_products,
    get_product,
    delete_product,
    update_product
)

router = APIRouter()


@router.get('/products/', response_model=List[ProductRead])
def read_all_products(db: Session = Depends(get_db)):
    products = get_products(db)
    return products


@router.get('/product/{product_id}', response_model=ProductRead)
def read_one_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id=product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    return product


@router.post("/products/", response_model=ProductRead)
def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db=db, product=product)


@router.delete('/product/{product_id}', response_model=ProductRead)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted_product = delete_product(db, product_id=product_id)
    if deleted_product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return deleted_product


@router.put('/product/{product_id}', response_model=ProductRead)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    added_product = update_product(db, product_id=product_id, product=product)
    if added_product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return added_product
