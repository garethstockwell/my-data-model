"""Utility functions."""

import importlib
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


def import_model_class(model_name: str, module_name: str, class_name: str) -> Any:
    """Import a class from a package.

    Args:
        model_name: name of model
        module_name: name of module within model package
        class_name: name of class within module

    Returns: class
    """
    module = importlib.import_module(f"my_data_model.models_{model_name}.{module_name}")
    return getattr(module, class_name)
