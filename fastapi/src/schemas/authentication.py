from pydantic import BaseModel, EmailStr
from typing import Optional

class RegistrationReq(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    password: str
    avatar: Optional[str] = None
    otp: Optional[int] = None
    role: Optional[str] = "user"  # Default to "user" if not provided
    isVerified: bool = False  # Default to False if not provided

class RegistrationRes(BaseModel):
    email: EmailStr
    name :str
    message: str

class OTPVerificationReq(BaseModel):
    email: EmailStr
    otp: str
