from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class SimulationStatus(Enum):
    NOT_VISITED = "not-visited"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class SimulationType(Enum):
    STACK = "stack"
    QUEUE = "queue"
    BINARY_TREE = "binary-tree"
    BINARY_SEARCH_TREE = "binary-search-tree"
    HANOI_TOWER = "hanoi-tower"
    FACTORIAL = "factorial"
    FIBONACCI = "fibonacci"


class Simulation(BaseModel):
    class Config:
        use_enum_values = True


class CreateSimulation(Simulation):
    type: SimulationType
    user_id: str
    status: SimulationStatus
    total_visits: int
    last_visit_at: datetime
    seconds_spent: float
    created_at: datetime
    updated_at: datetime


class UpdateSimulation(Simulation):
    status: Optional[SimulationStatus] = None
    total_visits: Optional[int] = None
    last_visit_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    seconds_spent: Optional[float] = None
    updated_at: datetime
