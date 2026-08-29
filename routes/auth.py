from fastapi import APIRouter, Depends, HTTPException
import db_models
from schemas import UserLogin
from sqlalchemy.orm import Session
from dependencies import get_db
from utils.jwt import create_access_token
from services.auth_service import authenticate_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = authenticate_user(user, db)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid Authentication")

    access_token = create_access_token(db_user.user_id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
