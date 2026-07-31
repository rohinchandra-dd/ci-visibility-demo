from sqlalchemy.orm import Session

from models.article import Article
from models.reaction import Reaction
from models.user import User


def add_reaction(
    db: Session,
    user: User,
    article: Article,
    reaction_type: str = "like",
) -> Reaction:
    existing = (
        db.query(Reaction)
        .filter(
            Reaction.user_id == user.id,
            Reaction.article_id == article.id,
            Reaction.reaction_type == reaction_type,
        )
        .first()
    )
    if existing:
        return existing
    reaction = Reaction(user_id=user.id, article_id=article.id, reaction_type=reaction_type)
    db.add(reaction)
    db.commit()
    db.refresh(reaction)
    return reaction


def remove_reaction(db: Session, user: User, article: Article, reaction_type: str = "like") -> bool:
    reaction = (
        db.query(Reaction)
        .filter(
            Reaction.user_id == user.id,
            Reaction.article_id == article.id,
            Reaction.reaction_type == reaction_type,
        )
        .first()
    )
    if not reaction:
        return False
    db.delete(reaction)
    db.commit()
    return True


def count_reactions(db: Session, article: Article, reaction_type: str = "like") -> int:
    return (
        db.query(Reaction)
        .filter(Reaction.article_id == article.id, Reaction.reaction_type == reaction_type)
        .count()
    )
