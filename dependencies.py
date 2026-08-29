from database import session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
import db_models


load_dotenv()

def get_db():
    with session() as db:
        yield db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):

    try:
        payload = jwt.decode(
            token, 
            os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    db_user = db.query(db_models.User).filter(
        db_models.User.user_id == int(user_id)
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return db_user