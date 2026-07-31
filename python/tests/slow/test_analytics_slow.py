"""Slow integration tests for analytics and search (~5 min total serial)."""

import time

import pytest

from services.analytics import generate_monthly_report, reindex_search
from services.articles import create_article
from services.users import create_user


@pytest.mark.slow
def test_analytics_fibonacci_benchmark(db_session):
    time.sleep(5)
    user = create_user(db_session, "slow1@pulse.dev", "slow1", "password123")
    create_article(db_session, user, "Slow Analytics", "body", published=True)
    report = generate_monthly_report(db_session, simulate_delay=True)
    assert report["benchmark"] == 6765


@pytest.mark.slow
@pytest.mark.parametrize("delay,index", [(5, 1), (8, 2), (6, 3), (7, 4), (5, 5)])
def test_search_reindex(db_session, delay, index):
    time.sleep(delay)
    user = create_user(db_session, f"reindex{index}@pulse.dev", f"reindex{index}", "password123")
    for i in range(3):
        create_article(db_session, user, f"Index {index}-{i}", "content", published=True)
    result = reindex_search(db_session, simulate_delay=False)
    assert result["status"] == "complete"


@pytest.mark.slow
@pytest.mark.parametrize("i", range(1, 16))
def test_monthly_report_batch(db_session, i):
    time.sleep(5)
    user = create_user(db_session, f"report{i}@pulse.dev", f"report{i}", "password123")
    create_article(db_session, user, f"Report {i}", "content", published=True)
    report = generate_monthly_report(db_session)
    assert report["published_articles"] >= 1


@pytest.mark.slow
def test_bulk_export_simulation(db_session):
    time.sleep(10)
    user = create_user(db_session, "export@pulse.dev", "export", "password123")
    for i in range(10):
        create_article(db_session, user, f"Export {i}", "data", published=True)
    report = generate_monthly_report(db_session)
    assert report["users"] >= 1
