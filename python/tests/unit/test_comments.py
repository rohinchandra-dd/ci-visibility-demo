"""Unit tests for comment service."""

from services.articles import create_article
from services.comments import create_comment, list_comments_for_article, moderate_comment
from services.users import create_user


def test_create_comment(db_session):
    user = create_user(db_session, "commenter@pulse.dev", "commenter", "password123")
    author = create_user(db_session, "author2@pulse.dev", "author2", "password123")
    article = create_article(db_session, author, "Post", "Body", published=True)
    comment = create_comment(db_session, user, article, "Great post!")
    assert comment.body == "Great post!"
    assert comment.article_id == article.id


def test_list_comments(db_session):
    user = create_user(db_session, "c1@pulse.dev", "c1", "password123")
    author = create_user(db_session, "a1@pulse.dev", "a1", "password123")
    article = create_article(db_session, author, "Comments Post", "Body", published=True)
    create_comment(db_session, user, article, "First")
    create_comment(db_session, user, article, "Second")
    comments = list_comments_for_article(db_session, article.id)
    assert len(comments) == 2


def test_moderate_comment(db_session):
    user = create_user(db_session, "mod@pulse.dev", "mod", "password123")
    author = create_user(db_session, "moda@pulse.dev", "moda", "password123")
    article = create_article(db_session, author, "Mod Post", "Body", published=True)
    comment = create_comment(db_session, user, article, "Bad words")
    moderated = moderate_comment(db_session, comment, "Edited")
    assert moderated.body == "Edited"
