from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskStatusUpdate


def get_task_by_id(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def list_tasks(db: Session, limit: int, offset: int, project_id: int | None = None):
    query = db.query(Task).order_by(Task.id.desc())
    if project_id is not None:
        query = query.filter(Task.project_id == project_id)
    return query.offset(offset).limit(limit).all()


def get_tasks_by_project(db: Session, project_id: int):
    return db.query(Task).filter(Task.project_id == project_id).order_by(Task.id.desc()).all()


def get_my_tasks(db: Session, user_id: int, project_id: int | None = None):
    query = db.query(Task).filter(Task.assigned_to == user_id).order_by(Task.id.desc())
    if project_id is not None:
        query = query.filter(Task.project_id == project_id)
    return query.all()


def get_tasks_for_user(db: Session, user_id: int):
    return db.query(Task).filter(Task.assigned_to == user_id).order_by(Task.due_date.desc()).all()


def create_task(db: Session, data: TaskCreate, created_by: int) -> Task:
    project = db.query(Project).filter(Project.id == data.project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if data.assigned_to is not None:
        # only assign to users who still have an active account
        user = db.query(User).filter(User.id == data.assigned_to, User.is_active == True).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assigned user not found or not active",
            )

    task = Task(
        title=data.title,
        description=data.description,
        status=data.status,
        priority=data.priority,
        due_date=data.due_date,
        project_id=data.project_id,
        assigned_to=data.assigned_to,
        created_by=created_by,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task: Task, data: TaskUpdate) -> Task:
    if data.project_id is not None:
        project = db.query(Project).filter(Project.id == data.project_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        task.project_id = data.project_id

    if data.assigned_to is not None:
        # same check during updates – prevent reassigning to inactive users
        user = db.query(User).filter(User.id == data.assigned_to, User.is_active == True).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assigned user not found or not active",
            )
        task.assigned_to = data.assigned_to

    if data.title is not None:
        task.title = data.title

    if data.description is not None:
        task.description = data.description

    if data.status is not None:
        task.status = data.status

    if data.priority is not None:
        task.priority = data.priority

    if data.due_date is not None:
        task.due_date = data.due_date

    db.commit()
    db.refresh(task)
    return task


def update_task_status_for_employee(db: Session, task: Task, current_user_id: int, data: TaskStatusUpdate) -> Task:
    if task.assigned_to != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update your own tasks")

    task.status = data.status
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()