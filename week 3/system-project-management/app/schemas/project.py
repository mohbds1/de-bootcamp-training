from datetime import datetime
from pydantic import BaseModel, ConfigDict

from .enums import ProjectStatus


class ProjectCreate(BaseModel):
    title: str
    description: str | None = None
    status: ProjectStatus = ProjectStatus.ACTIVE
    start_date: datetime | None = None
    end_date: datetime | None = None


class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: ProjectStatus | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: ProjectStatus
    owner_id: int
    created_at: datetime
    updated_at: datetime | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True)