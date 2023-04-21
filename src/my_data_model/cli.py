"""Command-line interface."""

import logging
import os
import sys
from pathlib import Path

import click

from my_data_model.io import load


DEFAULT_DATA_PATH = Path(os.path.dirname(__file__)) / "data" / "model.yaml"


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


@click.command()
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
@click.option("-v", "--verbose", is_flag=True)
def main(data_path: str, verbose: bool) -> None:
    """My Data Model."""
    _log_init(verbose)

    with open(data_path) as stream:
        data = load(stream=stream)

    print(data)


if __name__ == "__main__":
    main(prog_name="my-data-model")  # pragma: no cover
