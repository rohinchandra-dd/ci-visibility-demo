"""Unit tests for utility functions (migrated from legacy test_fast.py)."""

import pytest

from services.utils import (
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


def test_subtract_numbers():
    assert subtract(10, 4) == 6


def test_multiply_numbers():
    assert multiply(3, 7) == 21


def test_divide_numbers():
    assert divide(10, 2) == 5.0


def test_divide_by_zero_raises():
    with pytest.raises(ValueError):
        divide(1, 0)


def test_is_palindrome_simple():
    assert is_palindrome("racecar") is True


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


@pytest.mark.parametrize(
    "a,b,expected",
    [(1, 1, 2), (2, 3, 5), (10, 15, 25), (100, 200, 300), (-1, 1, 0)],
)
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
