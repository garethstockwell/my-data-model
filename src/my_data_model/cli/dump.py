"""Command which dumps the model to stdout."""

import logging
from pprint import pformat
from typing import Any

import click

from my_data_model.cli.main import command


@command
def dump(*args: Any, **kwargs: Any) -> None:
    """Command which dumps the model to stdout."""
    ctx = click.get_current_context()
    logging.info(pformat(ctx.obj))
