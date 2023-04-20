"""Test cases for the io module."""

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
    data = io.load(source=source, cls_prefix=__name__)
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
        AttributeError, match=f"module '{__name__}' has no attribute 'InvalidTag'"
    ):
        io.load(source=source, cls_prefix=__name__)


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
        io.load(source=source, cls_prefix=__name__)


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
        io.load(source=source, cls_prefix=__name__)


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
        io.load(source=source, cls_prefix=__name__)


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
        io.load(source=source, cls_prefix=__name__)