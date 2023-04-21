"""Commands."""

from typing import Mapping
from typing import get_args

from attrs import field
from attrs.validators import deep_mapping
from attrs.validators import instance_of

from my_data_model.models_attrs.common import model
from my_data_model.models_attrs.types import GeneralType
from my_data_model.utils import check_iterable_no_dups


@model
class CommandValue:
    """Command input or output value."""

    description: str = field(validator=[instance_of(str)])
    """Description of the command value."""

    name: str = field(validator=[instance_of(str)])
    """Name of the command value."""

    type: GeneralType = field(validator=[instance_of(get_args(GeneralType))])
    """Type of the command value."""


@model
class Command:
    """A command."""

    description: str = field(validator=[instance_of(str)])
    """Description of the command."""

    inputs: Mapping[str, CommandValue] = field(
        validator=[
            deep_mapping(
                # Check that keys are strings
                key_validator=instance_of(str),
                # Check that values are CommandValue instances
                value_validator=instance_of(CommandValue),
            ),
            # Check that input value names are unique
            lambda instance, attr, value: check_iterable_no_dups(
                name="input value names", data=[entry.name for entry in value.values()]
            ),
        ]
    )
    """Input values."""

    name: str = field(validator=[instance_of(str)])
    """Name of the command."""
