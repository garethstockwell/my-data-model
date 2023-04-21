"""Commands."""

from my_data_model.models_pydantic.common import model


@model
class Command:
    """A command."""

    name: str
    """Name of the command."""
