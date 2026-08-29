from fastapi import APIRouter, Depends, HTTPException
from schemas import OrderResponse, OrderCreate
from sqlalchemy.orm import Session
from dependencies import get_db
from services.user_service import find_user
from services.order_service import place_order_service, get_all_orders
from services import order_service

router = APIRouter(prefix="/user/{user_id}/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse)
def place_order(
    user_id: int,
    order: OrderCreate,
    db: Session = Depends(get_db)
):

    db_user =  find_user(user_id, db)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not identified")

    new_order = place_order_service(user_id, order.product_id, db)

    if not new_order:
        raise HTTPException(status_code=404, detail="Product not existing in inventory")

    return new_order


@router.get("", response_model= list[OrderResponse])
def get_all_orders(
    user_id: int,
    db: Session = Depends(get_db)
):

    db_user = find_user(user_id, db)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not there")

    return order_service.get_all_orders(db_user.user_id, db)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(
    user_id: int,
    order_id: int,
    db: Session = Depends(get_db)
):

    db_user = find_user(user_id, db)

    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")

    db_order = order_service.get_order_by_id(order_id, db)

    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    return db_order

