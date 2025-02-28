from pydantic import BaseModel, Field
from typing import Optional, List , Dict
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
        return str(v)  # Convert to string for Pydantic validation
    
class EventSchemaReq(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    name : Optional[str] 
    category : Optional[ObjectId]
    state : Optional[str]
    city : Optional[str]
    date : Optional[str]

    class Config:
        arbitrary_types_allowed = True

class EventSchemaRes(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    name : Optional[str]
    category : Optional[ObjectId]
    state : Optional[str]
    city : Optional[str]
    venue : Optional[str]
    date : Optional[str]
    description : Optional[str]
    price : Optional[float]

    class Config:
        arbitrary_types_allowed = True

class EventSchemaAdminReq(BaseModel):
    name : str
    category : str
    state : str
    city : str
    venue : str
    date : str
    description : str
    price : Dict[str , float]
    organizer : str
    tags : List[str]
    image : List[str]

    class Config:
        arbitrary_types_allowed = True