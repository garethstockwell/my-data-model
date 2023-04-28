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


def make_source(commands: int, inputs: int, tag: bool) -> str:
    """Make YAML source."""

    def make_tag(name: str, tag: bool) -> str:
        return f"!{name}" if tag else f"#{name}"

    def dedent(value: str) -> str:
        return textwrap.dedent(
            "\n".join(line for line in value.strip().split("\n") if line.strip())
        )

    def indent(prefix: str, value: str) -> str:
        space = " " * len(prefix)
        return prefix + ("\n" + space).join(value.split("\n"))

    def make_input(index: int, tag: bool) -> str:
        return dedent(
            f"""
{make_tag(name="commands.CommandValue", tag=tag)}
name: Input{index}
description: Example input {index}
type: {make_tag(name="types.Address", tag=tag)}
  name: Address
  description: An address
  width: 64
"""
        )

    def make_command(inputs: int, index: int, tag: bool) -> str:
        return dedent(
            f"""
{make_tag(name="commands.Command", tag=tag)}
name: Cmd{index}
description: Example command {index}
inputs:
"""
            + "\n".join(
                indent(f"  X{index}: ", make_input(index=index, tag=tag))
                for index in range(0, inputs)
            )
        )

    def make_interface(commands: int, inputs: int, tag: bool) -> str:
        return dedent(
            f"""
{make_tag(name="interfaces.Interface", tag=tag)}
name: Iface1
commands:
"""
            + "\n".join(
                indent(" - ", make_command(index=index, inputs=inputs, tag=tag))
                for index in range(0, commands)
            )
        )

    return make_interface(commands=commands, inputs=inputs, tag=tag)


def raw_load(source: str) -> Any:
    """Load raw data."""
    return yaml.safe_load(source)


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
    default=50,
    show_default=True,
)
@click.option(
    "-i",
    "--inputs",
    "inputs",
    help="Number of inputs",
    type=int,
    default=10,
    show_default=True,
)
@click.option(
    "-r",
    "--repeats",
    "repeats",
    help="Number of repeats",
    type=int,
    default=100,
    show_default=True,
)
def perf(*args: Any, **kwargs: Any) -> None:
    """Command which measures performance of model loading and validation."""
    ctx = click.get_current_context()

    commands = ctx.params["commands"]
    inputs = ctx.params["inputs"]
    repeats = ctx.params["repeats"]

    logging.info(f"Repeats   {repeats}")
    logging.info(f"Commands  {commands}")
    logging.info(f"Inputs    {inputs}")

    raw_source = make_source(commands=commands, inputs=inputs, tag=False)
    logging.debug(f"raw_source:\n{raw_source}")

    tagged_source = make_source(commands=commands, inputs=inputs, tag=True)
    logging.debug(f"tagged_source:\n{tagged_source}")

    start = time.time()
    for _i in range(0, repeats):
        data = raw_load(source=raw_source)
        logging.debug(data)
    end = time.time()
    elapsed = end - start
    logging.info(f"Total raw_load                {elapsed:.6f} s")
    average_raw = elapsed / repeats
    logging.info(f"Average raw_load              {average_raw:.6f} s")

    for model in ["attrs", "pydantic_bm", "pydantic_dc"]:
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
