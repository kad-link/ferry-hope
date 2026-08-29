from schemas import UserLogin
from sqlalchemy.orm import Session
from fastapi import Depends
from dependencies import get_db
import db_models
from utils.security import verify_password

def authenticate_user(
        user: UserLogin,
        db: Session = Depends(get_db)
):

    db_user = db.query(db_models.User).filter(
        db_models.User.email == user.user_email
    ).first()

    if not db_user:
        return None

    if not verify_password(user.user_password, db_user.password):
        return None

    return db_user