"""Test cases for the models_pydantic module."""

from typing import Any
from typing import List
from typing import Mapping

import pytest
from pydantic import ValidationError

from my_data_model.models_pydantic.commands import Command
from my_data_model.models_pydantic.commands import Interface


@pytest.mark.parametrize(
    "cls, kwargs",
    [
        # A command
        (Command, {"name": "my-cmd"}),
        # An interface with no commands
        (Interface, {"name": "my-iface", "commands": []}),
        # An interface with one command
        (
            Interface,
            {"name": "my-iface", "commands": [Command(name="my-cmd")]},
        ),
        # An interface with two distinctly-named commands
        (
            Interface,
            {
                "name": "my-iface",
                "commands": [
                    Command(name="my-cmd1"),
                    Command(name="my-cmd2"),
                ],
            },
        ),
    ],
)
def test_construct_good(cls: type, kwargs: Mapping[str, Any]) -> None:
    """Test successful construction of models.

    Args:
        cls: type of model to construct
        kwargs: dictionary of kwargs passed to constructor
    """
    cls(**kwargs)


if True:

    @pytest.mark.parametrize(
        "cls, kwargs, errors",
        [
            # A command with no name
            (
                Command,
                {},
                [("missing", tuple(["name"]))],
            ),
            # A command with a name of the incorrect type
            (
                Command,
                {"name": 123},
                [("string_type", tuple(["name"]))],
            ),
            # A command with an additional invalid argument
            (
                Command,
                {"name": "my-cmd", "foo": "bar"},
                [("unexpected_keyword_argument", tuple(["foo"]))],
            ),
            # An interface with no name
            (
                Interface,
                {"commands": []},
                [("missing", tuple(["name"]))],
            ),
            # An interface with a name of the incorrect type
            (
                Interface,
                {"name": 123, "commands": []},
                [("string_type", tuple(["name"]))],
            ),
            # An interface with no commands
            (
                Interface,
                {"name": "my-iface"},
                [("missing", tuple(["commands"]))],
            ),
            # An interface with wrongly typed commands
            (
                Interface,
                {"name": "my-iface", "commands": ["foo"]},
                [("dataclass_type", tuple(["commands", 0]))],
            ),
            # An interface with an additional invalid argument
            (
                Interface,
                {"name": "my-iface", "commands": [], "foo": "bar"},
                [("unexpected_keyword_argument", tuple(["foo"]))],
            ),
        ],
    )
    def test_construct_invalid_type(
        cls: type, kwargs: Mapping[str, Any], errors: List[Any]
    ) -> None:
        """Test failed construction of models due to invalid argument type(s).

        Args:
            cls: type of model to construct
            kwargs: dictionary of kwargs passed to constructor
            errors: expected errors
        """
        with pytest.raises(ValidationError) as excinfo:
            cls(**kwargs)

        assert [
            (error["type"], error["loc"]) for error in excinfo.value.errors()
        ] == errors


@pytest.mark.parametrize(
    "cls, kwargs, msg",
    [
        # An interface with two identically-named commands
        (
            Interface,
            {
                "name": "my-iface",
                "commands": [
                    Command(name="my-cmd"),
                    Command(name="my-cmd"),
                ],
            },
            "command names contains duplicate values: my-cmd",
        ),
    ],
)
def test_construct_invalid_value(
    cls: type, kwargs: Mapping[str, Any], msg: str
) -> None:
    """Test failed construction of models due to invalid argument value(s).

    Args:
        cls: type of model to construct
        kwargs: dictionary of kwargs passed to constructor
        msg: expected error message
    """
    with pytest.raises(ValueError, match=msg):
        cls(**kwargs)
