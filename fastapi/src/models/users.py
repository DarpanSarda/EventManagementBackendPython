from pydantic import BaseModel, EmailStr , Field
from typing import Optional

class Users(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    avatar: Optional[str] = None
    password: str = Field(..., min_length=8)
    otp: Optional[int] = None
    role: Optional[str] = "user"
    isVerified: bool = False