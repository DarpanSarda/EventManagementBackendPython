from pydantic import BaseModel, EmailStr , Field
from typing import Optional
from bson import ObjectId

class PyObjectId(str):
    """Custom Pydantic type for handling MongoDB ObjectId."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)  # Convert to string for JSON serialization


class Users(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    name: str
    lastname: str
    email: EmailStr
    avatar: Optional[str] = None
    password: str = Field(..., min_length=8)
    otp: Optional[int] = None
    role: Optional[str] = "user"
    isVerified: bool = False