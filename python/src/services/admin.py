from sqlalchemy.orm import Session

from models.comment import Comment
from models.user import User
from services.users import ban_user


def list_flagged_comments(db: Session, limit: int = 50) -> list[Comment]:
    return db.query(Comment).order_by(Comment.created_at.desc()).limit(limit).all()


def moderate_user(db: Session, user_id: int) -> User | None:
    return ban_user(db, user_id)


def moderation_queue_size(db: Session) -> int:
    return db.query(Comment).count()
