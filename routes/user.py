from fastapi import APIRouter, Depends
from schemas import UserResponse, UserCreate
from sqlalchemy.orm import Session
from dependencies import get_db
from services.user_service import create_user_service, get_all_users_service

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("", response_model= UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    return create_user_service(user, db)


@router.get("", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db)
):

    return get_all_users_service(db)