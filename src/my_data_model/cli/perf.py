"""Command which measures performance of model loading and validation."""

import logging
import textwrap
import time
from io import StringIO
from typing import Any

import click
import yaml

from my_data_model.cli.main import command
from my_data_model.io import load


def make_source(tag: bool) -> str:
    """Make YAML source."""

    def make_tag(name: str, tag: bool) -> str:
        return f"!{name}" if tag else ""

    def dedent(value: str) -> str:
        return textwrap.dedent(
            "\n".join(line for line in value.strip().split("\n") if line.strip())
        )

    def indent(prefix: str, value: str) -> str:
        space = " " * len(prefix)
        return prefix + ("\n" + space).join(value.split("\n"))

    def make_command(index: int, tag: bool) -> str:
        return dedent(
            f"""
{make_tag(name="commands.Command", tag=tag)}
name: Cmd{index}
description: Example command {index}
inputs: {{}}
"""
        )

    def make_interface(tag: bool) -> str:
        return dedent(
            f"""
{make_tag(name="interfaces.Interface", tag=tag)}
name: Iface1
commands:
{indent(" - ", make_command(index=0, tag=tag))}
{indent(" - ", make_command(index=1, tag=tag))}
"""
        )

    return make_interface(tag=tag)


def raw_load(source: str) -> Any:
    """Load raw data."""

    class SafeLoaderIgnoreUnknown(yaml.SafeLoader):
        def ignore_unknown(self, node):
            return None

    SafeLoaderIgnoreUnknown.add_constructor(
        None, SafeLoaderIgnoreUnknown.ignore_unknown
    )

    return yaml.load(  # type: ignore # nosec B506
        source, Loader=SafeLoaderIgnoreUnknown
    )


def model_load(source: str, model: str) -> Any:
    """Load, validate and create models."""
    with StringIO(source) as stream:
        return load(stream=stream, package=f"my_data_model.models_{model}")


@command
@click.option(
    "-c",
    "--commands",
    "commands",
    help="Number of commands",
    type=int,
    default=3,
    show_default=True,
)
@click.option(
    "-r",
    "--repeats",
    "repeats",
    help="Number of repeats",
    type=int,
    default=10000,
    show_default=True,
)
def perf(*args: Any, **kwargs: Any) -> None:
    """Command which measures performance of model loading and validation."""
    ctx = click.get_current_context()

    raw_source = make_source(tag=False)
    logging.debug(f"raw_source:\n{raw_source}")

    tagged_source = make_source(tag=True)
    logging.debug(f"tagged_source:\n{tagged_source}")

    repeats = ctx.params["repeats"]

    logging.info(f"Repeats                       {repeats}")

    start = time.time()
    for _i in range(0, repeats):
        data = raw_load(source=raw_source)
        logging.debug(data)
    end = time.time()
    elapsed = end - start
    logging.info(f"Total raw_load                {elapsed:.6f} s")
    average_raw = elapsed / repeats
    logging.info(f"Average raw_load              {average_raw:.6f} s")

    for model in ["attrs", "pydantic"]:
        logging.info("")
        start = time.time()
        for _i in range(0, repeats):
            data = model_load(source=tagged_source, model=model)
            logging.debug(data)
        end = time.time()
        elapsed = end - start
        logging.info(f"{model + ' total':30s}{elapsed:.6f} s")
        average_model = elapsed / repeats
        logging.info(f"{model + ' average':30s}{average_model:.6f} s")

        average_overhead = average_model - average_raw
        logging.info(f"{model + ' average overhead':30s}{average_overhead:.6f} s")
