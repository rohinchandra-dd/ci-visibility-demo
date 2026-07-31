from sqlalchemy.orm import Session

from models.article import Article
from models.tag import Tag, article_tags


def get_or_create_tag(db: Session, name: str) -> Tag:
    normalized = name.strip().lower()
    tag = db.query(Tag).filter(Tag.name == normalized).first()
    if tag:
        return tag
    tag = Tag(name=normalized)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def add_tag_to_article(db: Session, article: Article, tag_name: str) -> Tag:
    tag = get_or_create_tag(db, tag_name)
    if tag not in article.tags:
        article.tags.append(tag)
        db.commit()
        db.refresh(article)
    return tag


def search_articles(db: Session, query: str, limit: int = 20) -> list[Article]:
    pattern = f"%{query.lower()}%"
    return (
        db.query(Article)
        .filter(Article.published.is_(True))
        .filter((Article.title.ilike(pattern)) | (Article.body.ilike(pattern)))
        .limit(limit)
        .all()
    )


def list_tags(db: Session) -> list[Tag]:
    return db.query(Tag).order_by(Tag.name.asc()).all()


def articles_by_tag(db: Session, tag_name: str) -> list[Article]:
    return (
        db.query(Article)
        .join(article_tags)
        .join(Tag)
        .filter(Tag.name == tag_name.lower())
        .filter(Article.published.is_(True))
        .all()
    )
