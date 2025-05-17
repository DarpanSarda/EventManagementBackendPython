from pydantic import BaseModel, Field
from typing import Optional , Any
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

class PaymentSchemaReq(BaseModel):
    ticket_id: str
    user_id: str
    amount: float
    currency: str = "INR"


class PaymentSchemaRes(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    ticket_id: str
    user_id: str
    amount: float
    currency: str
    status: str
    razorpay_payment_id: Optional[str] = None
    razorpay_order_id: Optional[str] = None
    razorpay_signature: Optional[str] = None
    created_at: Optional[datetime] = None  # Made optional
    updated_at: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True  # Allow custom types like PyObjectId
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: str,  # For serializing ObjectId to string
        }

class VerifyPaymentSchema(BaseModel):
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str