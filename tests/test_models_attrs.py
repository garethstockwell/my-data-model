"""Test cases for the models_attrs module."""

from typing import Any
from typing import Mapping

import pytest

from my_data_model.models_attrs import Command
from my_data_model.models_attrs import Interface


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


@pytest.mark.parametrize(
    "cls, kwargs, msg",
    [
        # A command with no name
        (Command, {}, "missing 1 required positional argument: 'name'"),
        # A command with an additional invalid argument
        (
            Command,
            {"name": "my-cmd", "foo": "bar"},
            "got an unexpected keyword argument 'foo'",
        ),
        # An interface with no name
        (
            Interface,
            {"commands": []},
            "missing 1 required positional argument: 'name'",
        ),
        # An interface with no commands
        (
            Interface,
            {"name": "my-iface"},
            "missing 1 required positional argument: 'commands'",
        ),
        # An interface with wrongly typed commands
        (
            Interface,
            {"name": "my-iface", "commands": ["foo"]},
            "'commands' must be <class 'my_data_model.models_attrs.Command'>",
        ),
        # An interface with an additional invalid argument
        (
            Interface,
            {"name": "my-iface", "commands": [], "foo": "bar"},
            "got an unexpected keyword argument 'foo'",
        ),
    ],
)
def test_construct_invalid_type(cls: type, kwargs: Mapping[str, Any], msg: str) -> None:
    """Test failed construction of models due to invalid argument type(s).

    Args:
        cls: type of model to construct
        kwargs: dictionary of kwargs passed to constructor
        msg: expected error message
    """
    with pytest.raises(TypeError, match=msg):
        cls(**kwargs)


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
