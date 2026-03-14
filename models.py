from pydantic import BaseModel, Field
from typing import Optional

class user_model(BaseModel):
    UserName: str
    passw: str # Too short name, no validation
    email_address: str
    age: Optional[int] = None
    is_admin: bool = False # Dangerous default if used in registration

class Item(BaseModel):
    item_ID: int
    name: str = Field(..., min_length=1)
    description: str = ""
    Price: float # Inconsistent case
    category: str = "general"

class OrderItem(BaseModel):
    item_id: int
    quantity: int # Bug: missing validation (e.g., gt=0)
    price: float # Bug: missing validation

class OrderCreate(BaseModel):
    user_id: int # Bug: IDOR vulnerability potential if not verified against token
    items: list[OrderItem]
    total_amount: float
    status: str = "pending"

class LoginRequest(BaseModel):
    u: str
    p: str
