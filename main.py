from fastapi import FastAPI, Depends, HTTPException
from schemas import UserCreate, UserResponse, OrderResponse
from sqlalchemy.orm import Session
from dependencies import get_db
from db_models import User, Order
import db_models

app = FastAPI()


@app.post("/user", response_model= UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    new_user = User(
        user_name = user.user_name,
        email = user.user_email,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/user", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db)
):

    return db.query(db_models.User).all()


@app.post("/{user_id}/order", response_model=OrderResponse)
def place_order(
    user_id: int,
    product_id: int,
    db: Session = Depends(get_db)
):

    db_user = db.query(db_models.User).filter(
        db_models.User.user_id == user_id
    ).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not identified")

    db_product = db.query(db_models.Product).filter(
        db_models.Product.product_id == product_id
    ).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not existent yet")

    new_order = Order(
        ordered_by=user_id,
        product_id=product_id,
        status="Ordered"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


@app.get("/{user_id}/orders", response_model= list[OrderResponse])
def get_all_orders(
    user_id: int,
    db: Session = Depends(get_db)
):

    db_user = db.query(db_models.User).filter(
        db_models.User.user_id == user_id
    ).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not there")

    all_orders = db_user.orders

    return all_orders


@app.get("/{user_id}/orders/{order_id}", response_model=OrderResponse)
def get_order_by_id(
    user_id: int,
    order_id: int,
    db: Session = Depends(get_db)
):

    db_user = db.query(db_models.User).filter(
        db_models.User.user_id == user_id
    ).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")

    db_order = db.query(db_models.Order).filter(
        db_models.Order.order_id == order_id
    ).first()


    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    return db_order


