"""Test cases for the models_pydantic module with dataclasses."""

from typing import Any
from typing import List
from typing import Mapping

import pytest
from pydantic import ValidationError

from my_data_model.models_pydantic_dc.types import Array
from my_data_model.models_pydantic_dc.types import Bits
from tests.test_models import construct_good_data
from tests.test_models import construct_invalid_type_data
from tests.test_models import construct_invalid_value_data


TestBits64 = Bits(name="Bits64", description="A 64-bit field", width=64)
"""An address used for test purposes."""


@pytest.mark.parametrize("cls, kwargs", construct_good_data("pydantic_dc"))
def test_construct_good(cls: type, kwargs: Mapping[str, Any]) -> None:
    """Test successful construction of models.

    Args:
        cls: type of model to construct
        kwargs: dictionary of kwargs passed to constructor
    """
    cls(**kwargs)


@pytest.mark.parametrize(
    "cls, kwargs, errors", construct_invalid_type_data("pydantic_dc")
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

    assert [(error["type"], error["loc"]) for error in excinfo.value.errors()] == errors


@pytest.mark.parametrize(
    "cls, kwargs, errors", construct_invalid_value_data("pydantic_dc")
)
def test_construct_invalid_value(
    cls: type, kwargs: Mapping[str, Any], errors: str
) -> None:
    """Test failed construction of models due to invalid argument value(s).

    Args:
        cls: type of model to construct
        kwargs: dictionary of kwargs passed to constructor
        errors: expected error message
    """
    with pytest.raises(ValueError, match=errors):
        cls(**kwargs)


def test_array_width() -> None:
    """Test Array::width."""

    def make_array(size: int) -> Array:
        return Array(description="Array", name="array", size=size, type=TestBits64)

    assert make_array(size=0).width == 0
    assert make_array(size=1).width == 64
    assert make_array(size=2).width == 128
