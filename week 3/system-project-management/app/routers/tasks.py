from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth.deps import get_current_employee_or_manager, get_current_manager
from app.crud.tasks import (
    create_task,
    delete_task,
    get_my_tasks,
    get_task_by_id,
    list_tasks,
    update_task,
    update_task_status_for_employee,
)
from app.database import get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskStatusUpdate, TaskUpdate
from app.utils.pagination import pagination_params

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employee_or_manager),
    pg=Depends(pagination_params),
    project_id: int | None = Query(default=None),
):
    """
    Get all tasks.
    - Managers can see all tasks and filter by project.
    - Employees can only see their assigned tasks and filter them by project.
    """
    if current_user.role == "manager":
        return list_tasks(db, limit=pg["limit"], offset=pg["offset"], project_id=project_id)
    else:  # Employee
        return get_my_tasks(db, user_id=current_user.id, project_id=project_id)


@router.get("/{task_id}", response_model=TaskResponse)
def get_one_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employee_or_manager),
):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if current_user.role == "employee" and task.assigned_to != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this task")

    return task


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_one_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    return create_task(db, data, created_by=current_user.id)


@router.put("/{task_id}", response_model=TaskResponse)
def update_one_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return update_task(db, task, data)


@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_my_task_status(
    task_id: int,
    data: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employee_or_manager),
):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if current_user.role == "manager":
        task.status = data.status
        db.commit()
        db.refresh(task)
        return task

    return update_task_status_for_employee(db, task, current_user.id, data)


@router.delete("/{task_id}", status_code=204)
def delete_one_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    delete_task(db, task)
    return