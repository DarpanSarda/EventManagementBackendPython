from enum import Enum
from pydantic import BaseModel , Field, validator
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

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
    
class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"

class Offers(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    title: str
    bank_name: str
    discount_type: DiscountType
    discount_value: float  # Can be percentage or fixed amount
    short_detail: str
    image: str
    valid_till: datetime
    promo_code: str
    is_featured: bool = False
    minimum_order_value: float
    maximum_discount: float  # Cap for percentage discount
    valid_payment_methods: List[str]
    how_to_avail: List[str]
    terms_and_conditions: List[str]
    is_active: bool = True
    excluded_events: List[str] = []    
    cannot_combine: bool = True

    @validator('discount_value')
    def validate_discount(cls, v, values):
        if 'discount_type' in values:
            if values['discount_type'] == DiscountType.PERCENTAGE and (v < 0 or v > 100):
                raise ValueError("Percentage discount must be between 0 and 100")
            elif values['discount_type'] == DiscountType.FIXED and v < 0:
                raise ValueError("Fixed discount cannot be negative")
        return v
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}