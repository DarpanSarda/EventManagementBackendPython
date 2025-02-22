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
    error: Optional[str] = None
    token: Optional[str] = None
    tokenType: Optional[str] = None

class LoginReq(BaseModel):
    email: EmailStr
    password: str

class LoginRes(BaseModel):
    email: EmailStr
    message: Optional[str] = None
    error : Optional[str] = None
    token: Optional[str] = None
    tokenType: Optional[str] = None

class OTPVerificationReq(BaseModel):
    email: EmailStr
    otp: str
