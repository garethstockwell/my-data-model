"""Test cases for the cli module."""

from typing import List

import pytest
from click.testing import CliRunner

from my_data_model import cli


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


@pytest.mark.parametrize(
    "args",
    [
        [],
        ["dump"],
        ["dump", "--verbose"],
    ],
)
def test_main_succeeds(runner: CliRunner, args: List[str]) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(cli=cli.main, args=args)
    assert result.exit_code == 0
