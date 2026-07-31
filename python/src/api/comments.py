from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.deps import get_current_user
from core.database import get_db
from models.user import User
from services import articles as article_service
from services import comments as comment_service
from services import notifications as notification_service

router = APIRouter(prefix="/comments", tags=["comments"])


class CommentCreate(BaseModel):
    body: str
    article_id: int
    parent_id: int | None = None


class CommentResponse(BaseModel):
    id: int
    body: str
    article_id: int
    author_id: int
    parent_id: int | None

    class Config:
        from_attributes = True


@router.post("", response_model=CommentResponse, status_code=201)
def create_comment(
    payload: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    article = article_service.get_article_by_id(db, payload.article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    comment = comment_service.create_comment(
        db, current_user, article, payload.body, payload.parent_id
    )
    notification_service.notify_comment(db, article, current_user)
    return comment


@router.get("/article/{article_id}", response_model=list[CommentResponse])
def list_comments(article_id: int, db: Session = Depends(get_db)):
    return comment_service.list_comments_for_article(db, article_id)
