"""Test cases for the models module."""

from typing import Any

import pytest

from my_data_model import models
from my_data_model.models import Interface


@pytest.mark.parametrize(
    "cls, kwargs",
    [
        # A command
        (models.Command, {"name": "my-cmd"}),
        # An interface with no commands
        (models.Interface, {"name": "my-iface", "commands": []}),
        # An interface with one command
        (
            models.Interface,
            {"name": "my-iface", "commands": [models.Command(name="my-cmd")]},
        ),
        # An interface with two distinctly-named commands
        (
            models.Interface,
            {
                "name": "my-iface",
                "commands": [
                    models.Command(name="my-cmd1"),
                    models.Command(name="my-cmd2"),
                ],
            },
        ),
    ],
)
def test_construct_good(cls: type, kwargs: dict[str, Any]) -> None:
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
        (models.Command, {}, "missing 1 required positional argument: 'name'"),
        # A command with an additional invalid argument
        (
            models.Command,
            {"name": "my-cmd", "foo": "bar"},
            "got an unexpected keyword argument 'foo'",
        ),
        # An interface with no name
        (
            models.Interface,
            {"commands": []},
            "missing 1 required positional argument: 'name'",
        ),
        # An interface with no commands
        (
            models.Interface,
            {"name": "my-iface"},
            "missing 1 required positional argument: 'commands'",
        ),
        # An interface with wrongly typed commands
        (
            models.Interface,
            {"name": "my-iface", "commands": ["foo"]},
            "'commands' must be <class 'my_data_model.models.Command'>",
        ),
        # An interface with an additional invalid argument
        (
            models.Interface,
            {"name": "my-iface", "commands": [], "foo": "bar"},
            "got an unexpected keyword argument 'foo'",
        ),
    ],
)
def test_construct_invalid_type(cls: type, kwargs: dict[str, Any], msg: str) -> None:
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
            models.Interface,
            {
                "name": "my-iface",
                "commands": [
                    models.Command(name="my-cmd"),
                    models.Command(name="my-cmd"),
                ],
            },
            "command names contains duplicate values: my-cmd",
        ),
    ],
)
def test_construct_invalid_value(cls: type, kwargs: dict[str, Any], msg: str) -> None:
    """Test failed construction of models due to invalid argument value(s).

    Args:
        cls: type of model to construct
        kwargs: dictionary of kwargs passed to constructor
        msg: expected error message
    """
    with pytest.raises(ValueError, match=msg):
        cls(**kwargs)


@pytest.mark.parametrize(
    "kwargs, result",
    [
        (
            {
                "name": "my-iface",
                "commands": [],
            },
            {},
        ),
        (
            {
                "name": "my-iface",
                "commands": [
                    models.Command(name="cmd1"),
                ],
            },
            {
                "cmd1": models.Command(name="cmd1"),
            },
        ),
        (
            {
                "name": "my-iface",
                "commands": [
                    models.Command(name="cmd1"),
                    models.Command(name="cmd2"),
                ],
            },
            {
                "cmd1": models.Command(name="cmd1"),
                "cmd2": models.Command(name="cmd2"),
            },
        ),
    ],
)
def test_interface_commands_dict(kwargs: dict[str, Any], result: list[str]) -> None:
    """Test execution of Interface.commands_dict.

    Args:
        kwargs: dictionary of kwargs passed to constructor
        result: expected result
    """
    iface = Interface(**kwargs)
    assert iface.commands_dict == result
