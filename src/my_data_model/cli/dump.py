"""Command which dumps the model to stdout."""

import logging
from pprint import pformat
from typing import Any

import click

from my_data_model.cli.main import command
from my_data_model.io import load


@command
@click.option(
    "-m",
    "--model",
    "model",
    help="Model to use",
    type=click.Choice(["attrs", "pydantic_dc"]),
    default="attrs",
    show_default=True,
)
def dump(*args: Any, **kwargs: Any) -> None:
    """Command which dumps the model to stdout."""
    ctx = click.get_current_context()

    data_path = ctx.params["data_path"]
    model = ctx.params["model"]

    logging.info(f"Loading model {model} ...")

    package = f"my_data_model.models_{model}"

    with open(data_path) as stream:
        ctx.obj = load(stream=stream, package=package)

    logging.info(pformat(ctx.obj))
