from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth.deps import get_current_employee_or_manager, get_current_manager
from app.crud.projects import (
    create_project,
    delete_project,
    get_project_by_id,
    list_projects,
    list_projects_for_employee,
    update_project,
)
from app.database import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.utils.pagination import pagination_params

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employee_or_manager),
    pg=Depends(pagination_params),
    search: str | None = Query(default=None),
    status: str | None = Query(default=None),
):
    if current_user.role == "manager":
        return list_projects(
            db,
            limit=pg["limit"],
            offset=pg["offset"],
            search=search,
            status=status,
        )
    return list_projects_for_employee(
        db, current_user.id, search=search, status=status
    )


@router.get("/{project_id}", response_model=ProjectResponse)
def get_one_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employee_or_manager),
):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if current_user.role == "employee":
        # Check if the employee is assigned to any task in this project
        task_in_project = db.query(Task).filter(
            Task.project_id == project.id,
            Task.assigned_to == current_user.id
        ).first()
        if not task_in_project:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this project")

    return project


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_one_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    return create_project(db, owner_id=current_user.id, data=data)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_one_project(
    project_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return update_project(db, project, data)


@router.delete("/{project_id}", status_code=204)
def delete_one_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    delete_project(db, project)
    return