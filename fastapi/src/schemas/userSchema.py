from pydantic import BaseModel , EmailStr
from typing import Optional

class UserProfileRes(BaseModel):
    name: str
    email: EmailStr
    avatar: Optional[str] = None
    message: str