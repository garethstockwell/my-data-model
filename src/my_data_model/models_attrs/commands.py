"""Commands."""

from typing import List

from attrs import define
from attrs import field
from attrs.validators import deep_iterable
from attrs.validators import instance_of

from my_data_model.utils import check_iterable_no_dups


@define(frozen=True, slots=True)
class Command:
    """A command."""

    name: str = field(validator=[instance_of(str)])
    """Name of the command."""


@define(frozen=True, slots=True)
class Interface:
    """An interface."""

    name: str = field(validator=[instance_of(str)])
    """Name of the interface."""

    commands: List[Command] = field(
        validator=[
            # Check that members are Command instances
            deep_iterable(member_validator=instance_of(Command)),
            # Check that command names are unique
            lambda instance, attr, value: check_iterable_no_dups(
                name="command names", data=[cmd.name for cmd in value]
            ),
        ]
    )
    """Commands in the interface."""
