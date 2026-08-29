from schemas import UserCreate
from dependencies import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from db_models import User
from utils.security import hash_password
import db_models

def create_user_service(
        user: UserCreate,
        db: Session = Depends(get_db)
):

    new_user = User(
        user_name = user.user_name,
        email = user.user_email,
        password = hash_password(user.user_password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_all_users_service(
        db: Session = Depends(get_db)
):

    return db.query(db_models.User).all()


def find_user(
        user_id: int,
        db: Session = Depends(get_db)
):

    db_user = db.query(db_models.User).filter(
        db_models.User.user_id == user_id
    ).first()

    if not db_user:
        return None

    return db_user
