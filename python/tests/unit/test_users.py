"""Unit tests for user service."""

import pytest

from services.users import authenticate_user, create_user, get_user_by_email, update_user_profile


def test_create_user(db_session):
    user = create_user(db_session, "test@pulse.dev", "testuser", "password123")
    assert user.email == "test@pulse.dev"
    assert user.username == "testuser"


def test_authenticate_user(db_session):
    create_user(db_session, "auth@pulse.dev", "authuser", "password123")
    user = authenticate_user(db_session, "auth@pulse.dev", "password123")
    assert user is not None
    assert user.username == "authuser"


def test_duplicate_email_raises(db_session):
    create_user(db_session, "dup@pulse.dev", "user1", "password123")
    with pytest.raises(ValueError, match="Email already registered"):
        create_user(db_session, "dup@pulse.dev", "user2", "password123")


def test_update_profile(db_session):
    user = create_user(db_session, "profile@pulse.dev", "profileuser", "password123")
    updated = update_user_profile(db_session, user, bio="Hello Pulse")
    assert updated.bio == "Hello Pulse"


@pytest.mark.parametrize("email", [f"user{i}@pulse.dev" for i in range(20)])
def test_create_many_users(db_session, email):
    username = email.split("@")[0]
    user = create_user(db_session, email, username, "password123")
    assert get_user_by_email(db_session, email).id == user.id
