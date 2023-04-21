"""Interfaces."""

from typing import List

from pydantic import field_validator

from my_data_model.models_pydantic.commands import Command
from my_data_model.models_pydantic.common import model
from my_data_model.utils import check_iterable_no_dups


@model
class Interface:
    """An interface."""

    name: str
    """Name of the interface."""

    commands: List[Command]
    """Commands in the interface."""

    @field_validator("commands")
    def command_names_unique(
        cls, value: List[Command]  # types: ignore  # noqa: B902,N805
    ) -> List[Command]:
        """Check that command names are unique."""
        check_iterable_no_dups(name="command names", data=[cmd.name for cmd in value])
        return value
