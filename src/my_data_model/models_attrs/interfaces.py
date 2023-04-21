"""Interfaces."""

from typing import List

from attrs import field
from attrs.validators import deep_iterable
from attrs.validators import instance_of

from my_data_model.models_attrs.commands import Command
from my_data_model.models_attrs.common import model
from my_data_model.utils import check_iterable_no_dups


@model
class Interface:
    """An interface."""

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

    name: str = field(validator=[instance_of(str)])
    """Name of the interface."""
