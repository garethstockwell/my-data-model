"""Interfaces."""

from typing import List

from pydantic import field_validator

from my_data_model.models_pydantic.commands import Command
from my_data_model.models_pydantic.common import Model
from my_data_model.utils import check_iterable_no_dups


class Interface(Model):
    """An interface."""

    commands: List[Command]
    """Commands in the interface."""

    name: str
    """Name of the interface."""

    @field_validator("commands")
    def _command_names_unique(
        cls, value: List[Command]  # noqa: B902,N805
    ) -> List[Command]:
        """Check that command names are unique."""
        check_iterable_no_dups(name="command names", data=[cmd.name for cmd in value])
        return value
