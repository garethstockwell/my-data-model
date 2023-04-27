"""Common code shared across attrs models."""

from typing import Any

from attrs import define


def model(cls: type[Any]) -> type[Any]:
    """Declare an attrs dataclass model."""
    return define(
        maybe_cls=cls, auto_attribs=True, frozen=True, kw_only=True, slots=True
    )
