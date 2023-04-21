"""Types."""

from typing import Any
from typing import Union

from attrs import field
from attrs.validators import instance_of

from my_data_model.models_attrs.common import model


@model
class Type:
    """Base class for types."""


@model
class _WidthTemplatedType(Type):
    """Base class for types which are instantiated at different widths."""

    description: str = field(validator=[instance_of(str)])
    """Description of the type."""

    name: str = field(validator=[instance_of(str)])
    """Name of the type."""

    def _width_positive(self, _attr: Any, value: int) -> None:
        """Check that the width is positive."""
        if value <= 0:
            raise ValueError("width is not positive")

    width: int = field(validator=[instance_of(int), _width_positive])
    """Width of the type in bits."""


@model
class Address(_WidthTemplatedType):
    """An address type."""


@model
class Bits(_WidthTemplatedType):
    """A bitfield type."""


@model
class Array(Type):
    """Array type."""

    description: str = field(validator=[instance_of(str)])
    """Description of the type."""

    name: str = field(validator=[instance_of(str)])
    """Name of the type."""

    def _size_non_negative(self, _attr: Any, value: int) -> None:
        """Check that size is not negative."""
        if value < 0:
            raise ValueError("size is negative")

    size: int = field(validator=[instance_of(int), _size_non_negative])
    """Number of elements in the array."""

    type: Type = field(validator=[instance_of(Type)])
    """Type of elements in the array."""

    @property
    def width(self) -> int:
        """Width of the array in bits."""
        return self.size * self.type.width  # type: ignore [attr-defined,no-any-return]


GeneralType = Union[Address, Array, Bits]
"""Union of general types."""
