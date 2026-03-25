from datetime import datetime
from pydantic import BaseModel, ConfigDict

from .enums import TaskStatus, TaskPriority


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: datetime | None = None
    project_id: int
    assigned_to: int | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None
    project_id: int | None = None
    assigned_to: int | None = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: TaskStatus
    priority: TaskPriority
    due_date: datetime | None = None
    project_id: int
    assigned_to: int | None = None
    created_by: int | None = None
    created_at: datetime
    updated_at: datetime | None = None
    assigned_to_username: str | None = None  # visible when relationship is joined

    model_config = ConfigDict(from_attributes=True)