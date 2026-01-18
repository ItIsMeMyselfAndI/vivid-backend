from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class TimeSpentPayload(BaseModel):
    model_config = ConfigDict(extra="ignore")
    elapsed_secs: float = Field(ge=0)
    updated_at: datetime
