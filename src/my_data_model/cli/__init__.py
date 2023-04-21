"""Command-line interface."""

from my_data_model.cli.dump import dump
from my_data_model.cli.main import main


for command in [dump]:
    main.add_command(command)

__all__ = ["main"]
