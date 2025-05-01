from typing import TypeVar

T = TypeVar("T")

def chunked(items: list[T], chunk_size: int) -> list[list[T]]:
    """Returns groups of items from a larger sequence"""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

