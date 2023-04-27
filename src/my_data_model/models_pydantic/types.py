"""Types."""

from typing import Union

from pydantic import field_validator

from my_data_model.models_pydantic.common import Model


class Type(Model):
    """Base class for types."""


class _WidthTemplatedType(Type):
    """Base class for types which are instantiated at different widths."""

    description: str
    """Description of the type."""

    name: str
    """Name of the type."""

    width: int
    """Width of the type in bits."""

    @field_validator("width")
    def _width_positive(cls, value: int) -> int:  # noqa: B902,N805
        """Check that width is positive."""
        if value <= 0:
            raise ValueError("width is not positive")
        return value


class Address(_WidthTemplatedType):
    """An address type."""


class Bits(_WidthTemplatedType):
    """A bitfield type."""


class Array(Model):
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
    def _size_non_negative(cls, value: int) -> int:  # noqa: B902,N805
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
