from sqlalchemy.orm import Session

from models.article import Article
from models.comment import Comment
from models.user import User


def create_comment(
    db: Session,
    author: User,
    article: Article,
    body: str,
    parent_id: int | None = None,
) -> Comment:
    comment = Comment(
        body=body,
        article_id=article.id,
        author_id=author.id,
        parent_id=parent_id,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comment_by_id(db: Session, comment_id: int) -> Comment | None:
    return db.query(Comment).filter(Comment.id == comment_id).first()


def list_comments_for_article(db: Session, article_id: int) -> list[Comment]:
    return (
        db.query(Comment)
        .filter(Comment.article_id == article_id)
        .order_by(Comment.created_at.asc())
        .all()
    )


def delete_comment(db: Session, comment: Comment) -> None:
    db.delete(comment)
    db.commit()


def moderate_comment(db: Session, comment: Comment, new_body: str) -> Comment:
    comment.body = new_body
    db.commit()
    db.refresh(comment)
    return comment
