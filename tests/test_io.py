"""Test cases for the io module."""

from io import StringIO
from typing import Any
from typing import List
from typing import Mapping

import pytest
import yaml
from attrs import define

from my_data_model import io


@define(frozen=True, slots=True)
class MockObject:
    """A mock object."""

    attrs: Mapping[str, str]
    """Attributes of the object."""


@define(frozen=True, slots=True)
class MockCollection:
    """A mock collection."""

    objects: List[MockObject]
    """Objects in the collection."""


def load_str(source: str) -> Any:
    """Helper for loading data from a string."""
    with StringIO(source) as stream:
        return io.load(stream=stream, package=__name__)


def test_load_ok() -> None:
    """Test successful load."""
    source = """
    !MockCollection
    objects:
    - !MockObject
      attrs:
        foo: bar
    - !MockObject
      attrs:
        yah: gah
    """
    data = load_str(source=source)
    assert isinstance(data, MockCollection)
    assert data.objects == [
        MockObject(attrs={"foo": "bar"}),
        MockObject(attrs={"yah": "gah"}),
    ]


def test_load_invalid_tag() -> None:
    """Test load failure due to invalid tag."""
    source = """
    !InvalidTag
    foo: bar
    """
    with pytest.raises(
        AttributeError, match=f"module {__name__!r} has no attribute 'InvalidTag'"
    ):
        load_str(source=source)


def test_load_invalid_node_type() -> None:
    """Test load failure due to an invalid node type."""
    source = """
    !MockCollection
    - foo
    """
    with pytest.raises(
        yaml.constructor.ConstructorError,
        match="expected a mapping node, but found sequence",
    ):
        load_str(source=source)


def test_load_invalid_key() -> None:
    """Test load failure due to an invalid key."""
    source = """
    !MockCollection
    [foo]: bar
    """
    with pytest.raises(
        yaml.constructor.ConstructorError,
        match="found unacceptable key \\(unhashable type: 'list'\\)",
    ):
        load_str(source=source)


def test_load_duplicate_key() -> None:
    """Test load failure due to a duplicate key."""
    source = """
    !MockCollection
    foo: bar
    foo: bar
    """
    with pytest.raises(
        yaml.constructor.ConstructorError,
        match="found duplicate key",
    ):
        load_str(source=source)


def test_load_failed_construct() -> None:
    """Test load failure due to a constructor failure."""
    source = """
    !MockCollection
    foo: bar
    """
    with pytest.raises(
        TypeError,
        match="got an unexpected keyword argument 'foo'",
    ):
        load_str(source=source)


def test_load_invalid_include() -> None:
    """Test load failure due to invalid usage of include directive."""
    source = """
    !include foo.yaml
    """
    with pytest.raises(
        yaml.constructor.ConstructorError,
        match="Include directive not supported for f<file> loader",
    ):
        load_str(source=source)
