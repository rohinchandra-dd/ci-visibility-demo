"""Integration tests with database."""

import pytest

from services.analytics import article_stats, user_engagement
from services.articles import create_article
from services.comments import create_comment
from services.reactions import add_reaction, count_reactions
from services.search import add_tag_to_article, search_articles
from services.users import create_user


@pytest.mark.parametrize("tag_name", ["python", "javascript", "devops", "testing", "ci"])
def test_tag_and_search(db_session, tag_name):
    user = create_user(db_session, f"{tag_name}@pulse.dev", tag_name, "password123")
    article = create_article(db_session, user, f"{tag_name} post", "content", published=True)
    add_tag_to_article(db_session, article, tag_name)
    results = search_articles(db_session, tag_name)
    assert len(results) >= 1


def test_reaction_flow(db_session):
    user = create_user(db_session, "reactor@pulse.dev", "reactor", "password123")
    author = create_user(db_session, "ra@pulse.dev", "ra", "password123")
    article = create_article(db_session, author, "React", "Body", published=True)
    add_reaction(db_session, user, article)
    assert count_reactions(db_session, article) == 1


def test_analytics_stats(db_session):
    user = create_user(db_session, "stats@pulse.dev", "stats", "password123")
    article = create_article(db_session, user, "Stats", "word count test", published=True)
    stats = article_stats(db_session, article)
    assert stats["word_count"] == 3
    engagement = user_engagement(db_session, user)
    assert engagement["articles"] == 1


def test_comment_thread(db_session):
    author = create_user(db_session, "thread@pulse.dev", "thread", "password123")
    commenter = create_user(db_session, "tc@pulse.dev", "tc", "password123")
    article = create_article(db_session, author, "Thread", "Body", published=True)
    parent = create_comment(db_session, commenter, article, "Parent")
    reply = create_comment(db_session, commenter, article, "Reply", parent_id=parent.id)
    assert reply.parent_id == parent.id
