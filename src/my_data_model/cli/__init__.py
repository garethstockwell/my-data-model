"""Command-line interface."""

from my_data_model.cli.dump import dump
from my_data_model.cli.main import main
from my_data_model.cli.perf import perf


for command in [dump, perf]:
    main.add_command(command)

__all__ = ["main"]
