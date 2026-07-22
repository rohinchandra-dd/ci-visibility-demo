"""Flaky tests that fail intermittently for CI Visibility demos."""

import random

import pytest


@pytest.mark.flaky
def test_payment_gateway_timeout():
    if random.random() < 0.4:
        raise AssertionError("Gateway timeout after 30s")
    assert True
