from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class Profile(BaseModel):
    class Config:
        use_enum_values = True


class CreateProfile(Profile):
    id: str
    username: str
    email: EmailStr
    msg_of_the_day: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class UpdateProfile(Profile):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    msg_of_the_day: Optional[str] = None
    updated_at: datetime
