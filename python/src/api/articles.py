from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.deps import get_current_user
from core.database import get_db
from models.user import User
from services import articles as article_service

router = APIRouter(prefix="/articles", tags=["articles"])


class ArticleCreate(BaseModel):
    title: str
    body: str
    published: bool = False


class ArticleUpdate(BaseModel):
    title: str | None = None
    body: str | None = None


class ArticleResponse(BaseModel):
    id: int
    title: str
    slug: str
    body: str
    published: bool
    author_id: int

    class Config:
        from_attributes = True


@router.get("", response_model=list[ArticleResponse])
def list_articles(published_only: bool = True, db: Session = Depends(get_db)):
    return article_service.list_articles(db, published_only=published_only)


@router.post("", response_model=ArticleResponse, status_code=201)
def create_article(
    payload: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return article_service.create_article(
        db, current_user, payload.title, payload.body, payload.published
    )


@router.get("/{slug}", response_model=ArticleResponse)
def get_article(slug: str, db: Session = Depends(get_db)):
    article = article_service.get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.patch("/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    payload: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    article = article_service.get_article_by_id(db, article_id)
    if not article or article.author_id != current_user.id:
        raise HTTPException(status_code=404, detail="Article not found")
    return article_service.update_article(db, article, payload.title, payload.body)


@router.post("/{article_id}/publish", response_model=ArticleResponse)
def publish_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    article = article_service.get_article_by_id(db, article_id)
    if not article or article.author_id != current_user.id:
        raise HTTPException(status_code=404, detail="Article not found")
    return article_service.publish_article(db, article)
