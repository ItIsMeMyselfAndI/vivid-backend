from typing import Optional
from pydantic import BaseModel


class Visit(BaseModel):
    class Config:
        use_enum_values = True


class CreateVisit(Visit):
    page: str
    user_id: str


class UpdateVisit(Visit):
    page: Optional[str] = None
    user_id: Optional[str] = None
    hours_spent: Optional[float] = None
