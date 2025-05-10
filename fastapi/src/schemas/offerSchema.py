from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum

class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"

class OfferSchemaReq(BaseModel):
    title: str = Field(..., description="Offer title")
    bank_name: str = Field(..., description="Name of the bank offering the discount")
    discount_type: DiscountType
    discount_value: float = Field(..., description="Discount value (percentage or fixed amount)")
    short_detail: str = Field(..., description="Short description of the offer")
    image: str = Field(..., description="URL of the bank/offer image")
    valid_till: datetime = Field(..., description="Offer validity end date")
    promo_code: str = Field(..., description="Promotional code for the offer")
    minimum_order_value: float = Field(..., gt=0, description="Minimum order value to apply offer")
    maximum_discount: float = Field(..., gt=0, description="Maximum discount amount")
    valid_payment_methods: List[str] = Field(..., description="List of valid payment methods")
    how_to_avail: List[str] = Field(..., description="Steps to avail the offer")
    terms_and_conditions: List[str] = Field(..., description="Terms and conditions")
    is_featured: bool = Field(False, description="Whether the offer is featured")
    excluded_events: List[str] = Field(default=[], description="List of excluded event IDs")
    cannot_combine: bool = Field(True, description="Whether offer can be combined with others")

    @validator('discount_value')
    def validate_discount(cls, v, values):
        if 'discount_type' in values:
            if values['discount_type'] == DiscountType.PERCENTAGE and (v < 0 or v > 100):
                raise ValueError("Percentage discount must be between 0 and 100")
            elif values['discount_type'] == DiscountType.FIXED and v < 0:
                raise ValueError("Fixed discount cannot be negative")
        return v

class OfferSchemaRes(OfferSchemaReq):
    id: str = Field(..., alias="_id")
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "title": "10% Off on All Events",
                "bank_name": "HSBC Bank",
                "discount_type": "percentage",
                "discount_value": 10.0,
                "short_detail": "Get 10% instant discount on all event bookings",
                "image": "https://example.com/hsbc-logo.png",
                "valid_till": "2024-12-31T23:59:59",
                "promo_code": "HSBC10OFF",
                "minimum_order_value": 1000.0,
                "maximum_discount": 2000.0,
                "valid_payment_methods": ["HSBC Credit Card", "HSBC Debit Card"],
                "how_to_avail": [
                    "Select your preferred event",
                    "Apply promo code HSBC10OFF",
                    "Pay using HSBC card"
                ],
                "terms_and_conditions": [
                    "Valid on minimum purchase of ₹1000",
                    "Maximum discount ₹2000"
                ],
                "is_featured": True,
                "is_active": True,
                "excluded_events": [],
                "cannot_combine": True,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }