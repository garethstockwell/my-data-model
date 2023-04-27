"""Test cases for the models_attrs module."""

import importlib
from typing import Any
from typing import List


def import_class(model_name: str, module_name: str, class_name: str) -> Any:
    """Import a class from a package."""
    module = importlib.import_module(f"my_data_model.models_{model_name}.{module_name}")
    return getattr(module, class_name)


def address(model_name: str) -> Any:
    """Test address type."""
    Address = import_class(model_name, "types", "Address")  # noqa: N806
    return Address(name="Address", description="An address", width=64)


def construct_good_data(model_name: str) -> List[Any]:
    """Data for "construct_good" tests."""
    Command = import_class(model_name, "commands", "Command")  # noqa: N806
    CommandValue = import_class(model_name, "commands", "CommandValue")  # noqa: N806
    Interface = import_class(model_name, "interfaces", "Interface")  # noqa: N806

    return [
        # A command
        (
            Command,
            {
                "description": "Example command",
                "inputs": {
                    "X0": CommandValue(
                        description="Example input",
                        name="input1",
                        type=address(model_name),
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
    ]


def construct_invalid_type_data(model_name: str) -> List[Any]:
    """Data for "construct_invalid_type" tests."""
    Command = import_class(model_name, "commands", "Command")  # noqa: N806
    CommandValue = import_class(model_name, "commands", "CommandValue")  # noqa: N806
    Interface = import_class(model_name, "interfaces", "Interface")  # noqa: N806

    return [
        (cls, kwargs, errors[model_name])  # type: ignore
        for (cls, kwargs, errors) in [
            # A command value with no description
            (
                CommandValue,
                {
                    "name": "cmd",
                    "type": address(model_name),
                },
                {
                    "attrs": "missing 1 required keyword-only argument: 'description'",
                    "pydantic": [("missing", tuple(["description"]))],
                },
            ),
            # A command value with no name
            (
                CommandValue,
                {
                    "description": "Command value",
                    "type": address(model_name),
                },
                {
                    "attrs": "missing 1 required keyword-only argument: 'name'",
                    "pydantic": [("missing", tuple(["name"]))],
                },
            ),
            # A command value with no type
            (
                CommandValue,
                {
                    "description": "Command value",
                    "name": "cmd",
                },
                {
                    "attrs": "missing 1 required keyword-only argument: 'type'",
                    "pydantic": [("missing", tuple(["type"]))],
                },
            ),
            # A command value with a description of the incorrect type
            (
                CommandValue,
                {
                    "description": 123,
                    "name": "value",
                    "type": address(model_name),
                },
                {
                    "attrs": "'description' must be",
                    "pydantic": [("string_type", tuple(["description"]))],
                },
            ),
            # A command value with a name of the incorrect type
            (
                CommandValue,
                {
                    "description": "Command value",
                    "name": 123,
                    "type": address(model_name),
                },
                {
                    "attrs": "'name' must be",
                    "pydantic": [("string_type", tuple(["name"]))],
                },
            ),
            # A command value with a type of the incorrect type
            (
                CommandValue,
                {
                    "description": "Command value",
                    "name": "value",
                    "type": 123,
                },
                {
                    "attrs": "'type' must be",
                    "pydantic": [
                        ("dataclass_type", tuple(["type", "Address"])),
                        ("dataclass_type", tuple(["type", "Array"])),
                        ("dataclass_type", tuple(["type", "Bits"])),
                    ],
                },
            ),
            # A command with no description
            (
                Command,
                {
                    "inputs": {},
                    "name": "cmd",
                },
                {
                    "attrs": "missing 1 required keyword-only argument: 'description'",
                    "pydantic": [("missing", tuple(["description"]))],
                },
            ),
            # A command with no inputs
            (
                Command,
                {
                    "description": "Example command",
                    "name": "cmd",
                },
                {
                    "attrs": "missing 1 required keyword-only argument: 'inputs'",
                    "pydantic": [("missing", tuple(["inputs"]))],
                },
            ),
            # A command with no name
            (
                Command,
                {
                    "description": "Example command",
                    "inputs": {},
                },
                {
                    "attrs": "missing 1 required keyword-only argument: 'name'",
                    "pydantic": [("missing", tuple(["name"]))],
                },
            ),
            # A command with a description of the incorrect type
            (
                Command,
                {
                    "description": 123,
                    "inputs": {},
                    "name": "cmd",
                },
                {
                    "attrs": "'description' must be",
                    "pydantic": [("string_type", tuple(["description"]))],
                },
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
                            type=address(model_name),
                        ),
                        "X1": "foo",
                    },
                    "name": "cmd",
                },
                {
                    "attrs": "'inputs' must be",
                    "pydantic": [("dataclass_type", tuple(["inputs", "X1"]))],
                },
            ),
            # A command with a name of the incorrect type
            (
                Command,
                {
                    "description": "Example command",
                    "inputs": {},
                    "name": 123,
                },
                {
                    "attrs": "'name' must be",
                    "pydantic": [("string_type", tuple(["name"]))],
                },
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
                {
                    "attrs": "got an unexpected keyword argument 'foo'",
                    "pydantic": [("unexpected_keyword_argument", tuple(["foo"]))],
                },
            ),
            # An interface with no name
            (
                Interface,
                {
                    "commands": [],
                },
                {
                    "attrs": "missing 1 required keyword-only argument: 'name'",
                    "pydantic": [("missing", tuple(["name"]))],
                },
            ),
            # An interface with a name of the incorrect type
            (
                Interface,
                {
                    "commands": [],
                    "name": 123,
                },
                {
                    "attrs": "'name' must be <class 'str'>",
                    "pydantic": [("string_type", tuple(["name"]))],
                },
            ),
            # An interface with no commands
            (
                Interface,
                {
                    "name": "my-iface",
                },
                {
                    "attrs": "missing 1 required keyword-only argument: 'commands'",
                    "pydantic": [("missing", tuple(["commands"]))],
                },
            ),
            # An interface with a wrongly typed command
            (
                Interface,
                {
                    "commands": [
                        Command(
                            description="Example command", inputs={}, name="my-cmd1"
                        ),
                        "foo",
                    ],
                    "name": "my-iface",
                },
                {
                    "attrs": "'commands' must be",
                    "pydantic": [("dataclass_type", tuple(["commands", 1]))],
                },
            ),
            # An interface with an additional invalid argument
            (
                Interface,
                {
                    "commands": [],
                    "foo": "bar",
                    "name": "my-iface",
                },
                {
                    "attrs": "got an unexpected keyword argument 'foo'",
                    "pydantic": [("unexpected_keyword_argument", tuple(["foo"]))],
                },
            ),
        ]
    ]


def construct_invalid_value_data(model_name: str) -> List[Any]:
    """Data for "construct_invalid_type" tests."""
    Command = import_class(model_name, "commands", "Command")  # noqa: N806
    CommandValue = import_class(model_name, "commands", "CommandValue")  # noqa: N806
    Interface = import_class(model_name, "interfaces", "Interface")  # noqa: N806
    Address = import_class(model_name, "types", "Address")  # noqa: N806
    Array = import_class(model_name, "types", "Array")  # noqa: N806

    return [
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
                "type": address(model_name),
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
                        type=address(model_name),
                    ),
                    "X1": CommandValue(
                        description="Example input",
                        name="input",
                        type=address(model_name),
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
    ]
