from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username_or_email(db: Session, username_or_email: str) -> User | None:
    return db.query(User).filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()


def list_users(
    db: Session,
    limit: int,
    offset: int,
    search: str | None = None,
    role: str | None = None,
    is_active: bool | None = None,
):
    from sqlalchemy import or_

    query = db.query(User)
    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                User.username.ilike(term),
                User.email.ilike(term),
                User.full_name.ilike(term),
            )
        )
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    return query.order_by(User.id.asc()).offset(offset).limit(limit).all()


def create_user(db: Session, data: UserCreate) -> User:
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    if db.query(User).filter(User.email == str(data.email)).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    user = User(
        username=data.username,
        email=str(data.email),
        full_name=data.full_name,
        hashed_password=hash_password(data.password),
        role="employee",  # Hardcode role to prevent self-registration as manager
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, data: UserUpdate) -> User:
    if data.username is not None:
        existing = db.query(User).filter(User.username == data.username, User.id != user.id).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
        user.username = data.username

    if data.email is not None:
        existing = db.query(User).filter(User.email == str(data.email), User.id != user.id).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
        user.email = str(data.email)

    if data.full_name is not None:
        user.full_name = data.full_name

    if data.role is not None:
        if data.role not in ["manager", "employee"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
        user.role = data.role

    if data.is_active is not None:
        user.is_active = data.is_active

    db.commit()
    db.refresh(user)
    return user


def soft_delete_user(db: Session, user: User) -> None:
    user.is_active = False
    db.commit()