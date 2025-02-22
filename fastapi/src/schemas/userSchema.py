from pydantic import BaseModel
from typing import Optional

class UserProfileRes(BaseModel):
    name: Optional[str]
    email: Optional[str]
    avatar: Optional[str]
    message: Optional[str]
    error: Optional[str]