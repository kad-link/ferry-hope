from fastapi import APIRouter, Depends, HTTPException
from schemas import ProductResponse
from sqlalchemy.orm import Session
from dependencies import get_db
from services.product_service import get_all_products_service, get_product_by_id_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=list[ProductResponse])
def get_all_products(
    db: Session = Depends(get_db)
):
    return get_all_products_service(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db)
):
    db_product = get_product_by_id_service(product_id, db)

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    return db_product
