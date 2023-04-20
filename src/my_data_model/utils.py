"""Utility functions."""

from collections import Counter
from typing import Any
from typing import Iterable


def check_iterable_no_dups(name: str, data: Iterable[Any]) -> None:
    """Check that all elements of a collection are unique.

    Args:
        name: name of collection
        data: the collection

    Raises:
        ValueError: if collection contains duplicate elements
    """
    dups = [item for item, count in Counter(data).items() if count > 1]
    if dups:
        raise ValueError(f"{name} contains duplicate values: " + ", ".join(dups))
