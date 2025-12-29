from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class Profile(BaseModel):
    class Config:
        use_enum_values = True


class CreateProfile(Profile):
    id: str
    username: str
    email: EmailStr
    monthly_messages: Optional[List[str]] = []
    created_at: datetime
    updated_at: datetime


class UpdateProfile(Profile):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    monthly_messages: Optional[List[str]] = []
    updated_at: datetime
