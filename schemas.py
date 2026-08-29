from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class UserCreate(BaseModel):
    user_name: str
    user_email: str
    user_password: str

class UserResponse(BaseModel):
    user_id: int
    user_name: str
    email: str

class UserLogin(BaseModel):
    user_email: str
    user_password: str

class OrderCreate(BaseModel):
    product_id: int
class OrderResponse(BaseModel):
    order_id: int
    ordered_by: int
    product_id: int
    placed_at: datetime
    status: str

class AIRequest(BaseModel):
    message: str

class AIResponse(BaseModel):
    response: str

class OrderStatus(str, Enum):
    ORDERED = "ORDERED"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"