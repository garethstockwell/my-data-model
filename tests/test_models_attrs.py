"""Test cases for the models_attrs module."""

from typing import Any
from typing import Mapping

import pytest

from my_data_model.models_attrs.commands import Command
from my_data_model.models_attrs.commands import CommandValue
from my_data_model.models_attrs.interfaces import Interface
from my_data_model.models_attrs.types import Address
from my_data_model.models_attrs.types import Array
from my_data_model.models_attrs.types import Bits


TestAddress = Address(name="Address", description="An address", width=64)
"""An address used for test purposes."""

TestBits64 = Bits(name="Bits64", description="A 64-bit field", width=64)
"""An address used for test purposes."""


@pytest.mark.parametrize(
    "cls, kwargs",
    [
        # A command
        (
            Command,
            {
                "description": "Example command",
                "inputs": {
                    "X0": CommandValue(
                        description="Example input",
                        name="input1",
                        type=TestAddress,
                    )
                },
                "name": "my-cmd",
            },
        ),
        # An interface with no commands
        (Interface, {"name": "my-iface", "commands": []}),
        # An interface with one command
        (
            Interface,
            {
                "name": "my-iface",
                "commands": [
                    Command(description="Example command", inputs={}, name="my-cmd"),
                ],
            },
        ),
        # An interface with two distinctly-named commands
        (
            Interface,
            {
                "name": "my-iface",
                "commands": [
                    Command(description="Example command", inputs={}, name="my-cmd1"),
                    Command(description="Example command", inputs={}, name="my-cmd2"),
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
        # A command value with no description
        (
            CommandValue,
            {
                "name": "cmd",
                "type": TestAddress,
            },
            "missing 1 required positional argument: 'description'",
        ),
        # A command value with no name
        (
            CommandValue,
            {
                "description": "Command value",
                "type": TestAddress,
            },
            "missing 1 required positional argument: 'name'",
        ),
        # A command value with no type
        (
            CommandValue,
            {
                "description": "Command value",
                "name": "cmd",
            },
            "missing 1 required positional argument: 'type'",
        ),
        # A command value with a description of the incorrect type
        (
            CommandValue,
            {
                "description": 123,
                "name": "value",
                "type": TestAddress,
            },
            "'description' must be",
        ),
        # A command value with a description of the incorrect type
        (
            CommandValue,
            {
                "description": "Command value",
                "name": 123,
                "type": TestAddress,
            },
            "'name' must be",
        ),
        # A command value with a type of the incorrect type
        (
            CommandValue,
            {
                "description": "Command value",
                "name": "value",
                "type": 123,
            },
            "'type' must be",
        ),
        # A command with no description
        (
            Command,
            {
                "inputs": {},
                "name": "cmd",
            },
            "missing 1 required positional argument: 'description'",
        ),
        # A command with no inputs
        (
            Command,
            {
                "description": "Example command",
                "name": "cmd",
            },
            "missing 1 required positional argument: 'inputs'",
        ),
        # A command with no name
        (
            Command,
            {
                "description": "Example command",
                "inputs": {},
            },
            "missing 1 required positional argument: 'name'",
        ),
        # A command with a description of the incorrect type
        (
            Command,
            {
                "description": 123,
                "inputs": {},
                "name": "cmd",
            },
            "'description' must be",
        ),
        # A command with an input of the incorrect type
        (
            Command,
            {
                "description": "Example command",
                "inputs": {
                    "X0": CommandValue(
                        description="Example input",
                        name="input1",
                        type=TestAddress,
                    ),
                    "X1": "foo",
                },
                "name": "cmd",
            },
            "'inputs' must be",
        ),
        # A command with a name of the incorrect type
        (
            Command,
            {
                "description": "Example command",
                "inputs": {},
                "name": 123,
            },
            "'name' must be",
        ),
        # A command with an additional invalid argument
        (
            Command,
            {
                "description": "Example command",
                "foo": "bar",
                "inputs": {},
                "name": "cmd",
            },
            "got an unexpected keyword argument 'foo'",
        ),
        # An interface with no name
        (
            Interface,
            {
                "commands": [],
            },
            "missing 1 required positional argument: 'name'",
        ),
        # An interface with a name of the incorrect type
        (
            Interface,
            {
                "commands": [],
                "name": 123,
            },
            "'name' must be <class 'str'>",
        ),
        # An interface with no commands
        (
            Interface,
            {
                "name": "my-iface",
            },
            "missing 1 required positional argument: 'commands'",
        ),
        # An interface with a wrongly typed command
        (
            Interface,
            {
                "commands": [
                    Command(description="Example command", inputs={}, name="my-cmd1"),
                    "foo",
                ],
                "name": "my-iface",
            },
            "'commands' must be",
        ),
        # An interface with an additional invalid argument
        (
            Interface,
            {
                "commands": [],
                "foo": "bar",
                "name": "my-iface",
            },
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
        # A width-templated type with a non-positive width
        (
            Address,
            {
                "description": "Address",
                "name": "addr",
                "width": 0,
            },
            "width is not positive",
        ),
        # An array with a negative size
        (
            Array,
            {
                "description": "Array",
                "name": "array",
                "size": -1,
                "type": TestAddress,
            },
            "size is negative",
        ),
        # A command with identically-named input values
        (
            Command,
            {
                "description": "Example command",
                "inputs": {
                    "X0": CommandValue(
                        description="Example input",
                        name="input",
                        type=TestAddress,
                    ),
                    "X1": CommandValue(
                        description="Example input",
                        name="input",
                        type=TestAddress,
                    ),
                },
                "name": "my-cmd",
            },
            "input value names contains duplicate values: input",
        ),
        # An interface with identically-named commands
        (
            Interface,
            {
                "name": "my-iface",
                "commands": [
                    Command(description="Example command", inputs={}, name="my-cmd"),
                    Command(description="Example command", inputs={}, name="my-cmd"),
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


def test_array_width() -> None:
    """Test Array::width."""

    def make_array(size: int) -> Array:
        return Array(description="Array", name="array", size=size, type=TestBits64)

    assert make_array(size=0).width == 0
    assert make_array(size=1).width == 64
    assert make_array(size=2).width == 128
