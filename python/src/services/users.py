import re

from sqlalchemy.orm import Session

from core.auth import get_password_hash, verify_password
from models.user import User


def slugify_username(username: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", username.lower()).strip("-")


def create_user(db: Session, email: str, username: str, password: str) -> User:
    if db.query(User).filter(User.email == email).first():
        raise ValueError("Email already registered")
    if db.query(User).filter(User.username == username).first():
        raise ValueError("Username already taken")
    user = User(
        email=email,
        username=username,
        hashed_password=get_password_hash(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    if user.is_banned:
        return None
    return user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def update_user_profile(db: Session, user: User, bio: str | None = None) -> User:
    if bio is not None:
        user.bio = bio
    db.commit()
    db.refresh(user)
    return user


def ban_user(db: Session, user_id: int) -> User | None:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    user.is_banned = True
    db.commit()
    db.refresh(user)
    return user
