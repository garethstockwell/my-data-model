"""This module contains the data models, defined using pydantic."""

from typing import List

from pydantic import Extra
from pydantic import validator
from pydantic.dataclasses import dataclass

from my_data_model.utils import check_iterable_no_dups


class Config:
    """Configuration of dataclasses."""

    extra = Extra.forbid
    frozen = True
    validate_default = True


@dataclass(config=Config)
class Command:
    """A command."""

    name: str
    """Name of the command."""


@dataclass(config=Config)
class Interface:
    """An interface."""

    name: str
    """Name of the interface."""

    commands: List[Command]
    """Commands in the interface."""

    @validator("commands")
    def command_names_unique(
        cls, value: List[Command]  # types: ignore  # noqa: B902,N805
    ) -> None:
        """Check that command names are unique."""
        check_iterable_no_dups(name="command names", data=[cmd.name for cmd in value])
