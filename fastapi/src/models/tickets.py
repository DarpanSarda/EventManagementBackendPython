from pydantic import BaseModel, Field
from typing import Optional, List
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
    

class Ticket(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    persons: int
    status: str  # e.g., "pending", "confirmed", "cancelled"
    total_price: float
    purchase_date: datetime = Field(default_factory=datetime.now)
    attendee_info: Optional[List[str]]
    user: PyObjectId
    event: PyObjectId
    ticket_number: str
    payment_status: str
    payment_method: str
    qr_code: Optional[str]
    payment_id: Optional[PyObjectId]