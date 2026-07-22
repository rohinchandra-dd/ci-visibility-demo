"""Slow tests that simulate realistic integration-style workloads."""

import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import fibonacci


@pytest.mark.slow
def test_user_lookup_by_email():
    """Simulates a database query."""
    time.sleep(3)
    assert "user@example.com" in "user@example.com"


@pytest.mark.slow
def test_generate_monthly_report():
    """Simulates report aggregation."""
    time.sleep(8)
    assert sum(range(100)) == 4950


@pytest.mark.slow
def test_full_checkout_flow():
    """Simulates an end-to-end checkout flow."""
    time.sleep(15)
    assert "order_confirmed" == "order_confirmed"


@pytest.mark.slow
def test_bulk_import_records():
    """Simulates batch record processing."""
    time.sleep(12)
    assert len([1, 2, 3, 4, 5]) == 5


@pytest.mark.slow
def test_warm_cache_on_startup():
    """Simulates cache warming on service startup."""
    time.sleep(5)
    assert True


@pytest.mark.slow
def test_analytics_fibonacci_benchmark():
    """Simulates analytics workload that computes a fibonacci value."""
    time.sleep(5)
    assert fibonacci(30) == 832040
