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


class About(BaseModel):
    amenities: Optional[List[str]]
    lineup: Optional[List[str]]
    overview: Optional[str]

class Timings(BaseModel):
    eventEnd: Optional[str]
    gateOpening: Optional[str]
    lastEntry: Optional[str]

class AdditionalInfo(BaseModel):
    guidelines: Optional[List[str]]
    prohibited: Optional[List[str]]
    timings: Timings

class Slots(BaseModel):
    description: Optional[str]
    name: Optional[str]
    price: Optional[int]
    status: Optional[str]

class EventSchemaAdminReq(BaseModel):
    about: Optional[About]
    additionalInfo: Optional[AdditionalInfo]
    category: Optional[str]
    city: Optional[str]
    date: Optional[str]
    description: Optional[str]
    image: Optional[List[str]]
    organizer: Optional[str]
    price: Optional[int]
    slots: Optional[List[Slots]]
    state: Optional[str]
    tags: Optional[List[str]]
    time: Optional[str]
    title: Optional[str]
    venue: Optional[str]


    class Config:
        arbitrary_types_allowed = True