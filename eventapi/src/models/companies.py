from pydantic import BaseModel , Field
from typing import List , Optional
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


class Companies(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    name: str
    logo: str