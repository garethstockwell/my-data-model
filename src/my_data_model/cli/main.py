"""Command-line interface."""

import functools
import logging
import os
import sys
from pathlib import Path
from typing import Any

import click


DEFAULT_DATA_PATH = Path(os.path.dirname(__file__)).parent / "data" / "model.yaml"


def _log_init(verbose: bool) -> None:
    """Initialize logging."""

    class Formatter(logging.Formatter):
        def format(self, record):  # type: ignore # pragma: no cover
            format = "%(message)s"
            if record.levelno != logging.INFO:
                format = "[%(levelname)s] " + format
            return logging.Formatter(format).format(record)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(Formatter())
    logging.root.addHandler(handler)
    logging.root.setLevel(logging.DEBUG if verbose else logging.INFO)


class Command(click.Command):
    """Base class for commands."""

    def invoke(self, ctx: click.Context) -> Any:
        """Command entry point."""
        _log_init(verbose=ctx.params["verbose"])

        return super().invoke(ctx)


def command(func: Any) -> click.Command:
    """Decorator used to declare a command."""

    @click.command(cls=Command)
    @click.version_option()
    @click.option(
        "-d",
        "--data",
        "data_path",
        help="Path to data",
        metavar="PATH",
        default=DEFAULT_DATA_PATH,
        show_default=True,
    )
    @click.option(
        "-v", "--verbose", help="Increase verbosity of console output", is_flag=True
    )
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return wrapper


@click.group()
@click.version_option()
def main() -> None:
    """Main entry point."""
