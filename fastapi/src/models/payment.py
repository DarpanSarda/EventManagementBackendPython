from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
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
    

class Payment(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    ticket_id: PyObjectId
    user_id: PyObjectId
    amount: float
    currency: str = "INR"
    status: str  # e.g., "created", "completed", "failed"
    razorpay_payment_id: Optional[str] = None
    razorpay_order_id: Optional[str] = None
    razorpay_signature: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None