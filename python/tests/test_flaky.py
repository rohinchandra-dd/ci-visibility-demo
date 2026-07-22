"""Flaky tests that fail intermittently for CI Visibility demos."""

import random

import pytest


@pytest.mark.flaky
def test_payment_gateway_timeout():
    if random.random() < 0.4:
        raise AssertionError("Gateway timeout after 30s")
    assert True


@pytest.mark.flaky
def test_race_condition_on_inventory():
    if random.randint(0, 9) < 4:
        raise AssertionError("Expected stock=5, got stock=3")
    assert True


@pytest.mark.flaky
def test_third_party_api_rate_limit():
    if random.random() < 0.35:
        raise AssertionError("HTTP 429: Too Many Requests")
    assert True


@pytest.mark.flaky
def test_async_notification_delivery():
    if random.randint(0, 9) < 3:
        raise AssertionError("Notification not received within 5s")
    assert True


@pytest.mark.flaky
def test_concurrent_user_session():
    if random.random() < 0.38:
        raise AssertionError("Session token mismatch after concurrent writes")
    assert True
