import random

from sqlalchemy.orm import Session

from models.article import Article
from models.user import User


def send_notification(user: User, message: str) -> dict:
    """Simulate in-app notification delivery."""
    return {
        "user_id": user.id,
        "message": message,
        "delivered": True,
        "channel": "in_app",
    }


def send_email(user: User, subject: str, body: str) -> dict:
    """Simulate email delivery with occasional failures for flaky test demos."""
    success = random.random() > 0.38
    return {
        "user_id": user.id,
        "email": user.email,
        "subject": subject,
        "delivered": success,
        "channel": "email",
    }


def notify_comment(db: Session, article: Article, commenter: User) -> dict:
    author = db.query(User).filter(User.id == article.author_id).first()
    if not author or author.id == commenter.id:
        return {"skipped": True}
    message = f"{commenter.username} commented on {article.title}"
    in_app = send_notification(author, message)
    email = send_email(author, "New comment", message)
    return {"in_app": in_app, "email": email}
