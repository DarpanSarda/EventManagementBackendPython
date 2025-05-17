from pydantic import BaseModel, Field , ConfigDict
from typing import Optional, List, Dict ,Any
from datetime import datetime
from bson import ObjectId
from pydantic_core import core_schema

class PyObjectId(str):
    """Custom Pydantic type for handling MongoDB ObjectId."""
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.no_info_after_validator_function(cls.validate, core_schema.str_schema()),
            serialization=core_schema.plain_serializer_function_ser_schema(lambda x: str(x))
        )

    @classmethod
    def validate(cls, value: Any) -> str:
        if isinstance(value, ObjectId):
            return str(value)
        elif isinstance(value, str) and ObjectId.is_valid(value):
            return str(ObjectId(value))
        raise ValueError("Invalid ObjectId")


class AttendeeDetail(BaseModel):
    """Schema for attendee details"""
    name: str
    email: str
    phone: Optional[str] = None
    age: Optional[str] = None
    class Config:
        arbitrary_types_allowed = True

class BookingSchemaReq(BaseModel):
    """Schema for booking request"""
    user_id: str
    event_id: str
    slot_name: str
    quantity: int
    total_amount: float
    attendee_details: Optional[List[AttendeeDetail]] = None
    special_requests: Optional[str] = None
    class Config:
        arbitrary_types_allowed = True


class BookingSchemaRes(BaseModel):
    """Schema for booking response"""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_encoders={
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }
    )
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
    attendee_details: Optional[List[AttendeeDetail]] = None
    special_requests: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class BookingStatusUpdate(BaseModel):
    """Schema for booking status update"""
    status: str
    class Config:
        arbitrary_types_allowed = True


class BookingPaymentUpdate(BaseModel):
    """Schema for booking payment update"""
    payment_id: str
    ticket_id: Optional[str] = None
    class Config:
        arbitrary_types_allowed = True


class BookingListResponse(BaseModel):
    """Schema for list of bookings response"""
    total: int
    bookings: List[BookingSchemaRes]
    class Config:
        arbitrary_types_allowed = True