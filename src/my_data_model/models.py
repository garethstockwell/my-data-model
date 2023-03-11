"""This module contains the data models."""

from collections import Counter
from typing import Any
from typing import Iterable
from typing import List

from attrs import Attribute
from attrs import define
from attrs import field
from attrs.validators import deep_iterable
from attrs.validators import instance_of


def _unique_names(instance: Any, attribute: Attribute, value: Iterable[Any]) -> None:
    """Validator which enforces name uniqueness.

    Checks that all entries in an iterable have unique name attributes.

    Args:
        instance: parent of the attribute
        attribute: attribute which is being assigned to
        value: value which is being assigned to the attribute
    """
    names = [entry.name for entry in value]
    dups = [k for k, c in Counter(names).items() if c > 1]
    if dups:
        raise ValueError(f"Duplicate names in {attribute.name}: {','.join(dups)}")


@define
class Command:
    """A command."""

    name: str = field(validator=[instance_of(str)])
    """Name of the command."""


@define
class Interface:
    """An interface."""

    name: str = field(validator=[instance_of(str)])
    """Name of the interface."""

    commands: List[Command] = field(
        validator=[deep_iterable(member_validator=instance_of(Command)), _unique_names]
    )
    """Commands in the interface."""
