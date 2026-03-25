from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth.deps import get_current_manager, get_current_user
from app.crud.users import soft_delete_user, get_user_by_id, list_users, update_user
from app.crud.tasks import get_tasks_for_user
from app.crud.projects import list_projects_for_employee
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.task import TaskResponse
from app.schemas.project import ProjectResponse
from app.utils.pagination import pagination_params

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
    pg=Depends(pagination_params),
    search: str | None = Query(default=None),
    role: str | None = Query(default=None),
    is_active: bool | None = Query(default=None),
):
    return list_users(
        db,
        limit=pg["limit"],
        offset=pg["offset"],
        search=search,
        role=role,
        is_active=is_active,
    )


@router.get("/employees", response_model=list[UserResponse])
def get_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    users = list_users(db, limit=1000, offset=0)
    return [u for u in users if u.role == "employee"]


@router.get("/{user_id}", response_model=UserResponse)
def get_one_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}/tasks", response_model=list[TaskResponse])
def get_user_tasks(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return get_tasks_for_user(db, user_id)


@router.get("/{user_id}/projects", response_model=list[ProjectResponse])
def get_user_projects(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return list_projects_for_employee(db, user_id=user_id)


@router.put("/me", response_model=UserResponse)
def update_my_profile(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data.role is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot change your own role"
        )
    return update_user(db, current_user, data)


@router.delete("/me", status_code=204)
def delete_my_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    soft_delete_user(db, current_user)


@router.put("/{user_id}", response_model=UserResponse)
def update_user_admin(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    """Allow managers to update any user's profile, status, and role."""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Role change safeguards
    if data.role is not None and data.role != user.role:
        if data.role == "employee":
            # Demoting to employee
            if user_id == current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You cannot demote yourself. Promote another user first.",
                )
            if user.role == "manager":
                manager_count = db.query(User).filter(
                    User.role == "manager", User.is_active == True
                ).count()
                if manager_count <= 1:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Cannot demote the last manager. Promote another user first.",
                    )

    return update_user(db, user, data)


@router.delete("/{user_id}", status_code=204)
def delete_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    """Allow managers to soft-delete any user."""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    soft_delete_user(db, user)