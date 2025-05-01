import pytest
from rate_runner.runner.util import chunked

def test_chunked_less_than_chunk_size():
    items = [1, 2, 3]
    result = chunked(items, 10)
    assert result == [[1, 2, 3]]

def test_chunked_greater_than_chunk_size():
    items = list(range(15))
    result = chunked(items, 10)
    assert result == [list(range(10)), list(range(10, 15))]

def test_chunked_multiple_of_chunk_size():
    items = list(range(20))
    result = chunked(items, 10)
    assert result == [list(range(10)), list(range(10, 20))]

