"""Common code shared across pydantic models."""

from typing import Any

from pydantic.config import ConfigDict
from pydantic.dataclasses import dataclass


def model(cls: type[Any]) -> type[Any]:
    """Declare a pydantic dataclass model."""
    return dataclass(
        _cls=cls,
        config=ConfigDict(
            extra="forbid",
            frozen=True,
            validate_default=True,
        ),
    )
