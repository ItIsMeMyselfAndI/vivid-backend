from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class History(BaseModel):
    class Config:
        use_enum_values = True


class CreateHistory(History):
    page: str
    user_id: str
    opened_at: datetime


class UpdateHistory(History):
    page: Optional[str] = None
    opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
