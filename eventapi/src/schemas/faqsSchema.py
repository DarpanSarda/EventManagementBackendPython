from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any
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

class FAQsSchemaReq(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )
    
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    question: str = Field(min_length=1)
    answer: str = Field(min_length=1)