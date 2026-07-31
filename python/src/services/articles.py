import re

from sqlalchemy.orm import Session

from models.article import Article
from models.user import User


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:300] or "untitled"


def create_article(
    db: Session,
    author: User,
    title: str,
    body: str,
    published: bool = False,
) -> Article:
    base_slug = slugify(title)
    slug = base_slug
    counter = 1
    while db.query(Article).filter(Article.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1
    article = Article(
        title=title,
        slug=slug,
        body=body,
        published=published,
        author_id=author.id,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def get_article_by_id(db: Session, article_id: int) -> Article | None:
    return db.query(Article).filter(Article.id == article_id).first()


def get_article_by_slug(db: Session, slug: str) -> Article | None:
    return db.query(Article).filter(Article.slug == slug).first()


def list_articles(db: Session, published_only: bool = True, limit: int = 50) -> list[Article]:
    query = db.query(Article)
    if published_only:
        query = query.filter(Article.published.is_(True))
    return query.order_by(Article.created_at.desc()).limit(limit).all()


def update_article(db: Session, article: Article, title: str | None = None, body: str | None = None) -> Article:
    if title is not None:
        article.title = title
    if body is not None:
        article.body = body
    db.commit()
    db.refresh(article)
    return article


def publish_article(db: Session, article: Article) -> Article:
    article.published = True
    db.commit()
    db.refresh(article)
    return article


def delete_article(db: Session, article: Article) -> None:
    db.delete(article)
    db.commit()
