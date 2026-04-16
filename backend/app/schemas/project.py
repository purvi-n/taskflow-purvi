import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.task import TaskResponse

class ProjectBase(BaseModel):
    name: str
    description: str | None = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime

class ProjectDetailResponse(ProjectResponse):
    tasks: list[TaskResponse] = []

class ProjectStatsResponse(BaseModel):
    status_counts: dict[str, int]
    assignee_counts: dict[str, int]

