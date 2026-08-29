from schemas import UserResponse
from dependencies import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from db_models import Order
import db_models


def place_order_service(
        user_id: int,
        product_id: int,
        db: Session = Depends(get_db)
):

    db_product = db.query(db_models.Product).filter(
        db_models.Product.product_id == product_id
    ).first()

    if not db_product:
        return None

    new_order = Order(
        ordered_by=user_id,
        product_id=product_id,
        status="Ordered"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


def get_all_orders(
        user: UserResponse,
):

    return user.orders


def get_order_by_id(
        order_id: int,
        db: Session = Depends(get_db)
):

    db_product = db.query(db_models.Order).filter(
        db_models.Order.order_id == order_id
    ).first()

    if not db_product:
        return None

    return db_product