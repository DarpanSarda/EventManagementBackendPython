from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
import typing
from datetime import datetime


class PyObjectId(ObjectId):

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: typing.Any, _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            python_schema=core_schema.is_instance_schema(ObjectId),
            json_schema=core_schema.chain_schema(
                [
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x), return_schema=core_schema.str_schema()
            ),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class Audit(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    action: str
    timestamp: datetime  # ISO format string for datetime
    userId: PyObjectId
    details: str
    ip_adress: str
    status: str
    api_path: str
    eventId: Optional[PyObjectId] = None
    error_description: Optional[str] = None