from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Stats(BaseModel):
    class Config:
        use_enum_values = True


class CreateStats(Stats):
    user_id: str
    current_streak: int
    longest_streak: int
    seconds_spent: float
    created_at: datetime
    updated_at: datetime


class UpdateStats(Stats):
    current_streak: Optional[int] = None
    longest_streak: Optional[int] = None
    seconds_spent: Optional[float] = None
    updated_at: datetime
