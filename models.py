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

class LoginRequest(BaseModel):
    u: str
    p: str
