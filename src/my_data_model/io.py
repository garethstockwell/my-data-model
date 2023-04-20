"""YAML loader."""

import importlib
import logging
import os
from io import TextIOWrapper
from pathlib import Path
from typing import Any
from typing import Optional
from typing import Union

import yaml


LOGGER = logging.getLogger(__name__)


TAG_PREFIX = "!"
"""Prefix for YAML tags."""

MODELS_PACKAGE = "my_data_model.models"
"""Package from which models are loaded."""


class YamlLoader(yaml.Loader):
    """Override YAML loader."""

    def __init__(self, stream, cls_prefix):
        """Create YAML loader."""
        super().__init__(stream=stream)
        self.cls_prefix = cls_prefix

    def construct_mapping(self, node: yaml.MappingNode, deep: bool = True) -> Any:
        """Convert mapping node to dict or object.

        Override yaml.Loader for the following reasons:

        1. Makes a depth-first constructor by using deep=True by default.

        2. Raise exception when encountering duplicate keys.
        The exception is raised for the second key.

        3. Construct objects based on the tag.
        """
        LOGGER.debug(f"YamlLoader.construct_mapping node={node}")

        if not isinstance(node, yaml.MappingNode):
            raise yaml.constructor.ConstructorError(
                None,
                None,
                "expected a mapping node, but found %s" % node.id,
                node.start_mark,
            )

        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)  # type: ignore
            try:
                hash(key)
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "found unacceptable key (%s)" % exc,
                    key_node.start_mark,
                ) from exc
            if key in mapping:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping starting at",
                    node.start_mark,
                    "found duplicate key at",
                    key_node.start_mark,
                )
            value = self.construct_object(value_node, deep=deep)  # type: ignore
            mapping[key] = value

        cls = self._get_class(node.tag)
        if cls:
            try:
                return cls(**mapping)
            except Exception as exc:
                raise exc.__class__(
                    f"Failed to create object of type {cls.__module__}.{cls.__name__}\n"
                    f"from arguments {mapping}\n"
                    f"because {exc}"
                ) from exc
        return mapping

    def _get_class(self, tag: str) -> Any:
        """Look up class identified by a YAML tag."""
        if tag.startswith("!"):
            type_name = f"{self.cls_prefix}.{tag[len(TAG_PREFIX):]}"
            (module_name, cls_name) = type_name.rsplit(".", maxsplit=1)
            module = importlib.import_module(module_name)
            return getattr(module, cls_name)
        return None

    def include(self, node: yaml.Node) -> Any:
        """Process an include directive."""
        path = self.construct_scalar(node)

        LOGGER.debug(f"YamlLoader.include self.name={self.name} path={path}")

        if self.name in ["<unicode string>", "<byte string>", "<file>"]:
            raise yaml.constructor.ConstructorError(
                f"Include directive not supported for f{self.name} loader"
            )

        abs_path = Path(os.path.dirname(self.name)) / self.construct_scalar(node)

        def make_loader(stream):
            return YamlLoader(stream=stream, cls_prefix=self.cls_prefix)

        with open(abs_path) as stream:
            return yaml.load(stream, Loader=make_loader)  # nosec B506


def load(
    source: Union[str, TextIOWrapper],
    cls_prefix: Optional[str] = None,
) -> Any:
    """Load data from YAML.

    Args:
        source: data source
        cls_prefix: string which is prepended to YAML tag to form class name
        include_base: base directory for include directives
    """
    cls_prefix = cls_prefix or MODELS_PACKAGE

    loader = YamlLoader

    loader.add_constructor("!include", loader.include)

    loader.add_multi_constructor(
        tag_prefix=TAG_PREFIX,
        multi_constructor=lambda loader, _tag, node: loader.construct_mapping(
            node, deep=True
        ),
    )  # type: ignore

    def make_loader(stream):
        return YamlLoader(stream=stream, cls_prefix=cls_prefix)

    # The source for the YAML load is a local file whose contents we can trust.
    return yaml.load(source, Loader=make_loader)  # nosec B506
