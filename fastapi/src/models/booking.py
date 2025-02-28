from pydantic import BaseModel , Field
from typing import List , Optional
from models.users import Users
from models.event import Event
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
    user : PyObjectId
    event : PyObjectId
    bookingDate : str
    status : str
    totalAmount : float
    totalTickets : int
    adults : List[str]
    children : List[str]