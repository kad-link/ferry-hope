from sqlalchemy.orm import Session
from db_models import Order
import db_models
from schemas import OrderStatus


def place_order_service(
        user_id: int,
        product_id: int,
        db: Session 
):

    db_product = db.query(db_models.Product).filter(
        db_models.Product.product_id == product_id
    ).first()

    if not db_product:
        return None

    new_order = Order(
        ordered_by=user_id,
        product_id=product_id,
        status=OrderStatus.ORDERED
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


def get_all_orders(
        user_id: int,
        db: Session 
):

    return db.query(db_models.Order).filter(
        db_models.Order.ordered_by == user_id
    ).all()


def get_order_by_id(
        order_id: int,
        user_id: int,
        db: Session 
):

    return db.query(db_models.Order).filter(
        db_models.Order.order_id == order_id,
        db_models.Order.ordered_by == user_id
    ).first()


def mark_delivered(
        order_id: int,
        user_id: int,
        db: Session
):

    db_order = db.query(db_models.Order).filter(
        db_models.Order.order_id == order_id,
        db_models.Order.ordered_by == user_id
    ).first()

    db_order.status = OrderStatus.DELIVERED

    return db_order.status


def cancel_order(
        order_id: int,
        user_id: int,
        db: Session
):

    db_order = db.query(db_models.Order).filter(
            db_models.Order.order_id == order_id,
            db_models.Order.ordered_by == user_id
        ).first()
    
    db_order.status = OrderStatus.CANCELED
    
    return db_order.status