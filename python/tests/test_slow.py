"""Slow tests that simulate realistic integration-style workloads."""

import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import fibonacci


@pytest.mark.slow
def test_analytics_fibonacci_benchmark():
    """Simulates analytics workload that computes a fibonacci value."""
    time.sleep(5)
    assert fibonacci(30) == 832040
