import time

from sqlalchemy.orm import Session

from models.article import Article
from models.reaction import Reaction
from models.user import User
from services.utils import fibonacci


def article_stats(db: Session, article: Article) -> dict:
    reaction_count = db.query(Reaction).filter(Reaction.article_id == article.id).count()
    return {
        "article_id": article.id,
        "reactions": reaction_count,
        "word_count": len(article.body.split()),
    }


def user_engagement(db: Session, user: User) -> dict:
    article_count = db.query(Article).filter(Article.author_id == user.id).count()
    reaction_count = db.query(Reaction).filter(Reaction.user_id == user.id).count()
    return {
        "user_id": user.id,
        "articles": article_count,
        "reactions": reaction_count,
    }


def generate_monthly_report(db: Session, simulate_delay: bool = False) -> dict:
    if simulate_delay:
        time.sleep(5)
    users = db.query(User).count()
    articles = db.query(Article).filter(Article.published.is_(True)).count()
    return {
        "users": users,
        "published_articles": articles,
        "benchmark": fibonacci(20),
    }


def reindex_search(db: Session, simulate_delay: bool = False) -> dict:
    if simulate_delay:
        time.sleep(8)
    articles = db.query(Article).filter(Article.published.is_(True)).all()
    return {"indexed": len(articles), "status": "complete"}
