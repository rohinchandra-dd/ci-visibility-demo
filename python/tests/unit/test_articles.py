"""Unit tests for article service."""

import pytest

from services.articles import create_article, get_article_by_slug, list_articles, publish_article, slugify
from services.users import create_user


def test_slugify():
    assert slugify("Hello World") == "hello-world"


def test_create_and_publish_article(db_session):
    user = create_user(db_session, "author@pulse.dev", "author", "secret123")
    article = create_article(db_session, user, "First Post", "Hello Pulse", published=False)
    assert article.published is False
    published = publish_article(db_session, article)
    assert published.published is True


def test_list_published_only(db_session):
    user = create_user(db_session, "writer@pulse.dev", "writer", "secret123")
    create_article(db_session, user, "Draft", "draft body", published=False)
    create_article(db_session, user, "Live", "live body", published=True)
    published = list_articles(db_session, published_only=True)
    assert len(published) == 1
    assert published[0].title == "Live"


@pytest.mark.parametrize("title,expected_slug", [
    ("Getting Started", "getting-started"),
    ("Python 3.12 Tips", "python-3-12-tips"),
    ("CI/CD Best Practices", "ci-cd-best-practices"),
])
def test_slugify_titles(title, expected_slug):
    assert slugify(title) == expected_slug
