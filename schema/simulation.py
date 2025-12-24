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
    RECURSION = "recursion"


class Simulation(BaseModel):
    class Config:
        use_enum_values = True


class CreateSimulation(Simulation):
    type: SimulationType
    user_id: str
    status: SimulationStatus
    current_streak: int
    longest_streak: int
    total_visits: int
    last_visit_at: datetime
    hours_spent: float


class UpdateSimulation(Simulation):
    status: Optional[SimulationStatus] = None
    current_streak: Optional[int] = None
    longest_streak: Optional[int] = None
    total_visits: Optional[int] = None
    last_visit_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    hours_spent: Optional[float] = None
