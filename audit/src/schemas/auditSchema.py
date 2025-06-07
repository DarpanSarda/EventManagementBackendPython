from typing import Optional, Annotated
from pydantic import BaseModel, BeforeValidator
from bson import ObjectId


# Validator to ensure ObjectId is valid and convert it to string
def validate_object_id(v):
    if not ObjectId.is_valid(v):
        raise ValueError("Invalid ObjectId")
    return str(v)

# Annotated custom ObjectId type
PyObjectId = Annotated[str, BeforeValidator(validate_object_id)]

    
class Audit(BaseModel):
    action: str
    timestamp: str
    userId: PyObjectId
    details: str
    ip_adress: str
    status: str
    api_path: str
    eventId: Optional[PyObjectId] = None
    error_description: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}