"""Commands."""

from typing import Mapping

from pydantic import field_validator

from my_data_model.models_pydantic.common import Model
from my_data_model.models_pydantic.types import GeneralType
from my_data_model.utils import check_iterable_no_dups


class CommandValue(Model):
    """Command input or output value."""

    description: str
    """Description of the command value."""

    name: str
    """Name of the command value."""

    type: GeneralType
    """Type of the command value."""


class Command(Model):
    """A command."""

    description: str
    """Description of the command."""

    inputs: Mapping[str, CommandValue]
    """Input values."""

    name: str
    """Name of the command."""

    @field_validator("inputs")
    def _validate_inputs(
        cls, value: Mapping[str, CommandValue]  # noqa: B902,N805
    ) -> Mapping[str, CommandValue]:
        """Validate inputs."""
        check_iterable_no_dups(
            name="input value names", data=[entry.name for entry in value.values()]
        )
        return value
