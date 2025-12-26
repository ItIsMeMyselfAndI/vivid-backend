from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class SettingsTheme(Enum):
    DARK = "dark"
    LIGHT = "light"


class Settings(BaseModel):
    class Config:
        use_enum_values = True


class CreateSettings(Settings):
    theme: SettingsTheme
    speed: float
    user_id: str
    created_at: datetime
    updated_at: datetime


class UpdateSettings(Settings):
    theme: Optional[SettingsTheme] = None
    speed: Optional[float] = None
    updated_at: datetime
