"""Types."""

from typing import Union

from pydantic import field_validator

from my_data_model.models_pydantic.common import model


@model
class Type:
    """Base class for types."""


@model
class _WidthTemplatedType(Type):
    """Base class for types which are instantiated at different widths."""

    description: str
    """Description of the type."""

    name: str
    """Name of the type."""

    width: int
    """Width of the type in bits."""

    @field_validator("width")
    def width_positive(cls, value: int) -> int:  # noqa: B902,N805
        """Check that width is positive."""
        if value <= 0:
            raise ValueError("width is not positive")
        return value


@model
class Address(_WidthTemplatedType):
    """An address type."""


@model
class Bits(_WidthTemplatedType):
    """A bitfield type."""


@model
class Array(Type):
    """Array type."""

    description: str
    """Description of the type."""

    name: str
    """Name of the type."""

    size: int
    """Number of elements in the array."""

    type: Type
    """Type of elements in the array."""

    @field_validator("size")
    def size_non_negative(cls, value: int) -> int:  # noqa: B902,N805
        """Check that size is not negative."""
        if value < 0:
            raise ValueError("size is negative")
        return value

    @property
    def width(self) -> int:
        """Width of the array in bits."""
        return self.size * self.type.width  # type: ignore [attr-defined,no-any-return]


GeneralType = Union[Address, Array, Bits]
"""Union of general types."""
