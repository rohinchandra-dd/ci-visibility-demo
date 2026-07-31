"""Flaky tests simulating intermittent failures."""

import random

import pytest

from services.notifications import send_email, send_notification
from services.users import create_user


@pytest.mark.flaky
def test_payment_gateway_timeout(db_session):
    user = create_user(db_session, "flaky1@pulse.dev", "flaky1", "password123")
    result = send_email(user, "Payment", "Your payment is processing")
    if not result["delivered"]:
        pytest.fail("Payment gateway timeout")


@pytest.mark.flaky
@pytest.mark.parametrize("i", range(1, 6))
def test_email_delivery(db_session, i):
    user = create_user(db_session, f"flakyemail{i}@pulse.dev", f"flakyemail{i}", "password123")
    result = send_email(user, f"Subject {i}", f"Body {i}")
    if random.random() < 0.38 and not result["delivered"]:
        pytest.fail("Email delivery failed")


@pytest.mark.flaky
def test_notification_race(db_session):
    user = create_user(db_session, "race@pulse.dev", "race", "password123")
    result = send_notification(user, "Race condition test")
    if random.random() < 0.35:
        pytest.fail("Notification race detected")


@pytest.mark.flaky
@pytest.mark.parametrize("i", range(1, 4))
def test_rate_limit(db_session, i):
    user = create_user(db_session, f"rate{i}@pulse.dev", f"rate{i}", "password123")
    if random.random() < 0.4:
        pytest.fail("Rate limit exceeded")
