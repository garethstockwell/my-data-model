"""YAML loader."""

import importlib
import logging
import os
from io import IOBase
from pathlib import Path
from typing import Any
from typing import Optional

import yaml


LOGGER = logging.getLogger(__name__)


_TAG_PREFIX = "!"
"""Prefix for YAML tags."""

DEFAULT_PACKAGE = "my_data_model.models_attrs"
"""Default package from which models are loaded."""


class _YamlLoader(yaml.Loader):
    """Override YAML loader."""

    def __init__(self, stream: IOBase, package: str):
        """Create YAML loader."""
        super().__init__(stream=stream)
        self.package = package

    def construct_mapping(self, node: yaml.Node, deep: bool = True) -> Any:
        """Convert mapping node to dict or object.

        Override yaml.Loader for the following reasons:

        1. Makes a depth-first constructor by using deep=True by default.

        2. Raise exception when encountering duplicate keys.
        The exception is raised for the second key.

        3. Construct objects based on the tag.
        """
        LOGGER.debug(f"_YamlLoader.construct_mapping node={node}")

        if not isinstance(node, yaml.MappingNode):
            raise yaml.constructor.ConstructorError(
                context=None,
                context_mark=None,
                problem=f"expected a mapping node, but found {node.id}",  # type: ignore
                problem_mark=node.start_mark,
                note=None,
            )

        mapping = {}

        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)  # type: ignore

            try:
                hash(key)
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    context="while constructing a mapping",
                    context_mark=node.start_mark,
                    problem=f"found unacceptable key '{key}' ({exc})",  # noqa: B907
                    problem_mark=key_node.start_mark,
                    note=None,
                ) from exc

            if key in mapping:
                raise yaml.constructor.ConstructorError(
                    context="while constructing a mapping",
                    context_mark=node.start_mark,
                    problem=f"found duplicate key '{key}'",  # noqa: B907
                    problem_mark=key_node.start_mark,
                    note=None,
                )

            value = self.construct_object(value_node, deep=deep)  # type: ignore
            mapping[key] = value

        cls = self._get_class(node.tag)
        if cls:
            try:
                return cls(**mapping)
            except Exception as exc:
                raise yaml.constructor.ConstructorError(
                    context=None,
                    context_mark=None,
                    problem=f"failed to create {cls.__module__}.{cls.__name__}:\n{exc}",
                    problem_mark=node.start_mark,
                    note=None,
                ) from exc

        return mapping

    def _get_class(self, tag: str) -> Any:
        """Look up class identified by a YAML tag."""
        if tag.startswith("!"):
            type_name = f"{self.package}.{tag[len(_TAG_PREFIX):]}"
            (module_name, cls_name) = type_name.rsplit(".", maxsplit=1)
            module = importlib.import_module(module_name)
            return getattr(module, cls_name)

        return None

    def include(self, node: yaml.ScalarNode) -> Any:
        """Process an include directive."""
        path = str(self.construct_scalar(node))

        LOGGER.debug(f"_YamlLoader.include self.name={self.name} path={path}")

        if self.name in ["<unicode string>", "<byte string>", "<file>"]:
            raise yaml.constructor.ConstructorError(
                context=None,
                context_mark=None,
                problem=f"'!include' tag not supported for f{self.name} loader",
                problem_mark=node.start_mark,
                note=None,
            )

        abs_path = (Path(os.path.dirname(self.name)) / path).resolve()

        def make_loader(stream: IOBase) -> yaml.Loader:
            return _YamlLoader(stream=stream, package=self.package)

        with open(abs_path) as stream:
            return yaml.load(
                stream=stream, Loader=make_loader  # type: ignore # nosec B506
            )


def load(
    stream: IOBase,
    package: Optional[str] = None,
) -> Any:
    """Load data from YAML.

    Args:
        stream: data source
        package: package from which models are loaded, defaults to
                 :const:`~my_data_model.io.DEFAULT_PACKAGE`

    Returns:
        Data loaded from YAML
    """
    my_package = package or DEFAULT_PACKAGE

    loader = _YamlLoader

    loader.add_constructor("!include", loader.include)

    loader.add_multi_constructor(
        tag_prefix=_TAG_PREFIX,
        multi_constructor=lambda loader, _tag, node: loader.construct_mapping(
            node, deep=True
        ),
    )  # type: ignore

    def make_loader(stream: IOBase) -> yaml.Loader:
        return _YamlLoader(stream=stream, package=my_package)

    return yaml.load(stream=stream, Loader=make_loader)  # type: ignore # nosec B506
