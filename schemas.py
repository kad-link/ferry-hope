from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    user_name: str
    user_email: str


class UserResponse(BaseModel):
    user_id: int
    user_name: str
    email: str

class OrderCreate(BaseModel):
    product_id: int
class OrderResponse(BaseModel):
    order_id: int
    ordered_by: int
    product_id: int
    placed_at: datetime
    status: str
