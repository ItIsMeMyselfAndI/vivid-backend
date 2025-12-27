from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class History(BaseModel):
    class Config:
        use_enum_values = True


class CreateHistory(History):
    page: str
    user_id: str
    seconds_spent: float
    created_at: datetime
    updated_at: datetime


class UpdateHistory(History):
    page: Optional[str] = None
    seconds_spent: Optional[float] = None
    updated_at: datetime
