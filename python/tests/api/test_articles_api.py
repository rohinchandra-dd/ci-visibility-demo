"""API integration tests."""

from services.articles import create_article
from services.users import create_user


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "pulse-api"


def test_register_and_login(client):
    register = client.post(
        "/api/auth/register",
        json={"email": "api@pulse.dev", "username": "apiuser", "password": "secret123"},
    )
    assert register.status_code == 200
    login = client.post(
        "/api/auth/login",
        json={"email": "api@pulse.dev", "password": "secret123"},
    )
    assert login.status_code == 200
    assert "access_token" in login.json()


def test_create_article_api(client, auth_headers):
    response = client.post(
        "/api/articles",
        json={"title": "API Article", "body": "Content", "published": True},
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["title"] == "API Article"


def test_list_articles_api(client, auth_headers):
    client.post(
        "/api/articles",
        json={"title": "Listed", "body": "Body", "published": True},
        headers=auth_headers,
    )
    response = client.get("/api/articles")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_search_api(client, auth_headers):
    client.post(
        "/api/articles",
        json={"title": "Searchable Topic", "body": "find me", "published": True},
        headers=auth_headers,
    )
    response = client.get("/api/search?q=Searchable")
    assert response.status_code == 200
    assert len(response.json()) >= 1
