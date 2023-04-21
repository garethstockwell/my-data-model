"""Commands."""

from attrs import field
from attrs.validators import instance_of

from my_data_model.models_attrs.common import model


@model
class Command:
    """A command."""

    name: str = field(validator=[instance_of(str)])
    """Name of the command."""
