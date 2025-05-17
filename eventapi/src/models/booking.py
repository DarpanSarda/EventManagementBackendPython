from pydantic import BaseModel, Field
from typing import Optional, List, Dict
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


class Booking(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    user_id: PyObjectId
    event_id: PyObjectId
    ticket_id: Optional[PyObjectId] = None
    payment_id: Optional[PyObjectId] = None
    booking_number: str
    slot_name: str
    quantity: int
    total_amount: float
    status: str
    booking_date: datetime
    attendee_details: Optional[List[Dict[str, str]]]
    special_requests: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None