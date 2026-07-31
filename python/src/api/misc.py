from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.deps import get_current_user
from core.database import get_db
from models.user import User
from services import articles as article_service
from services import reactions as reaction_service
from services import search as search_service

router = APIRouter(tags=["misc"])


class TagRequest(BaseModel):
    name: str


class ReactionResponse(BaseModel):
    article_id: int
    reaction_type: str
    count: int


@router.get("/tags")
def list_tags(db: Session = Depends(get_db)):
    return [{"name": t.name, "id": t.id} for t in search_service.list_tags(db)]


@router.post("/articles/{article_id}/tags")
def add_tag(
    article_id: int,
    payload: TagRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    article = article_service.get_article_by_id(db, article_id)
    if not article or article.author_id != current_user.id:
        return {"error": "not found"}
    tag = search_service.add_tag_to_article(db, article, payload.name)
    return {"name": tag.name}


@router.get("/search")
def search(q: str, db: Session = Depends(get_db)):
    articles = search_service.search_articles(db, q)
    return [{"id": a.id, "title": a.title, "slug": a.slug} for a in articles]


@router.post("/articles/{article_id}/reactions", response_model=ReactionResponse)
def react(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    article = article_service.get_article_by_id(db, article_id)
    if not article:
        return ReactionResponse(article_id=article_id, reaction_type="like", count=0)
    reaction_service.add_reaction(db, current_user, article)
    count = reaction_service.count_reactions(db, article)
    return ReactionResponse(article_id=article_id, reaction_type="like", count=count)
