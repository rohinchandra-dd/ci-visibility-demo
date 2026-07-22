"""Fast unit tests for demo CI Visibility."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import (
    add,
    clamp,
    chunk_list,
    divide,
    fibonacci,
    flatten,
    is_palindrome,
    merge_dicts,
    multiply,
    subtract,
)


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -1) == -2


def test_subtract_numbers():
    assert subtract(10, 4) == 6


def test_multiply_numbers():
    assert multiply(3, 7) == 21


def test_divide_numbers():
    assert divide(10, 2) == 5.0


def test_divide_by_zero_raises():
    try:
        divide(1, 0)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_is_palindrome_simple():
    assert is_palindrome("racecar") is True


def test_is_palindrome_with_spaces():
    assert is_palindrome("A man a plan a canal Panama") is True


def test_is_palindrome_not_palindrome():
    assert is_palindrome("hello") is False


def test_fibonacci_zero():
    assert fibonacci(0) == 0


def test_fibonacci_one():
    assert fibonacci(1) == 1


def test_fibonacci_ten():
    assert fibonacci(10) == 55


def test_flatten_nested_list():
    assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]


def test_chunk_list_even():
    assert chunk_list([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_merge_dicts():
    assert merge_dicts({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}


def test_clamp_within_range():
    assert clamp(5, 0, 10) == 5


def test_clamp_below_minimum():
    assert clamp(-5, 0, 10) == 0


def test_clamp_above_maximum():
    assert clamp(15, 0, 10) == 10


def test_fibonacci_negative_raises():
    try:
        fibonacci(-1)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_chunk_list_odd_length():
    assert chunk_list([1, 2, 3], 2) == [[1, 2], [3]]


def test_chunk_list_zero_size_raises():
    try:
        chunk_list([1, 2, 3], 0)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_merge_dicts_key_collision():
    assert merge_dicts({"a": 1}, {"a": 2}) == {"a": 2}


def test_is_palindrome_empty_string():
    assert is_palindrome("") is True


def test_flatten_empty_list():
    assert flatten([]) == []


def test_user_profile_merge():
    profile = merge_dicts({"email": "user@example.com"}, {"name": "User"})
    assert profile == {"email": "user@example.com", "name": "User"}


def test_monthly_report_total():
    assert add(multiply(50, 99), 0) == 4950


def test_checkout_order_total():
    subtotal = multiply(25, 3)
    total = add(subtotal, 5)
    assert total == 80


def test_bulk_import_batching():
    records = [1, 2, 3, 4, 5]
    assert chunk_list(records, 2) == [[1, 2], [3, 4], [5]]


def test_cache_warmup_fibonacci():
    assert fibonacci(12) == 144


def test_inventory_stock_decrement():
    stock = subtract(5, 2)
    assert clamp(stock, 0, 10) == 3


def test_api_retry_backoff_clamp():
    assert clamp(120, 1, 60) == 60


def test_notification_payload_merge():
    payload = merge_dicts({"status": "sent"}, {"recipient": "user@example.com"})
    assert payload == {"status": "sent", "recipient": "user@example.com"}


def test_session_token_merge():
    session = merge_dicts({"token": "abc"}, {"token": "xyz"})
    assert session == {"token": "xyz"}
