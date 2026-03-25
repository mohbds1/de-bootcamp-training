from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


def get_project_by_id(db: Session, project_id: int) -> Project | None:
    return db.query(Project).filter(Project.id == project_id).first()


def list_projects(
    db: Session,
    limit: int,
    offset: int,
    search: str | None = None,
    status: str | None = None,
):
    query = db.query(Project)
    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            Project.title.ilike(term) | Project.description.ilike(term)
        )
    if status:
        query = query.filter(Project.status == status)
    return query.order_by(Project.id.desc()).offset(offset).limit(limit).all()


def create_project(db: Session, owner_id: int, data: ProjectCreate) -> Project:
    project = Project(
        title=data.title,
        description=data.description,
        status=data.status,
        owner_id=owner_id,
        start_date=data.start_date,
        end_date=data.end_date,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def update_project(db: Session, project: Project, data: ProjectUpdate) -> Project:
    if data.title is not None:
        project.title = data.title

    if data.description is not None:
        project.description = data.description

    if data.status is not None:
        project.status = data.status

    if data.start_date is not None:
        project.start_date = data.start_date

    if data.end_date is not None:
        project.end_date = data.end_date

    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project: Project) -> None:
    db.delete(project)
    db.commit()


def list_projects_for_employee(
    db: Session,
    user_id: int,
    search: str | None = None,
    status: str | None = None,
):
    from app.models.task import Task

    query = (
        db.query(Project)
        .join(Task, Task.project_id == Project.id)
        .filter(Task.assigned_to == user_id)
        .distinct()
    )
    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            Project.title.ilike(term) | Project.description.ilike(term)
        )
    if status:
        query = query.filter(Project.status == status)
    return query.order_by(Project.id.desc()).all()