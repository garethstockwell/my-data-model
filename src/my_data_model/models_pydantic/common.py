"""Common code shared across pydantic models."""

from pydantic import BaseModel


class Model(BaseModel):
    """Base class for models."""

    model_config = {
        "extra": "forbid",
        "frozen": True,
        "validate_default": True,
    }
