"""Test cases for the cli module."""

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
def test_main_succeeds(runner: CliRunner, args) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(cli.main, *args)
    assert result.exit_code == 0
