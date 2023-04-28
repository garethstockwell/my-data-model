# My Data Model

[![PyPI](https://img.shields.io/pypi/v/my-data-model.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/my-data-model.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/my-data-model)][pypi status]
[![License](https://img.shields.io/pypi/l/my-data-model)][license]

[![Read the documentation at https://my-data-model.readthedocs.io/](https://img.shields.io/readthedocs/my-data-model/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/garethstockwell/my-data-model/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/garethstockwell/my-data-model/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/my-data-model/
[read the docs]: https://my-data-model.readthedocs.io/
[tests]: https://github.com/garethstockwell/my-data-model/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/garethstockwell/my-data-model
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features

This package is an investigation into the use of various frameworks for defining a data model.
The goals of the investigation were to determine the following, for each framework:

- The ease of use of the programming model
- The quality of documentation which can be generated to describe the schema of the model
- The runtime cost of data validation and model creation

The example model is a collection of interface definitions, where:

- Each interface has a name, a description and a list of commands.
- Each command has a name, a description and a dictionary which maps register names to input value definitions.
- Each input value has a name, a description and a type.

The model data is loaded from YAML files (see `src/my_data_model/data`) and used to create model objects.
Each model class defines a schema against which the incoming data is validated.
For example, if the data for an interface lacks a name, validation fails and an error is raised.

The frameworks which have been used are:

- [attrs]
- [pydantic]

Both frameworks support definition of models as Python dataclasses.
[pydantic] also provides a `BaseModel` class from which models can inherit, as an alternative to using dataclasses.
The choice between `dataclass` and `BaseModel` has an associated set of tradeoffs, which are described [in the pydantic documentation][pydantic-dataclasses].

## Installation

You can install _My Data Model_ via [pip]:

```console
$ pip install .
```

## Usage

### CLI

The package provides a CLI with the following commands:

- `my-data-model dump`: load and validate data, then print to the console
- `my-data-model perf`: measure the cost of data validation and model creation, for each framework

Please see the [Command-line Reference] for further details of the commands.

### Tests

To execute tests, run

```console
$ nox -s tests
```

The following additional `nox` flags may be useful during development, both for `tests` and other sessions:

- `-r`: reuse existing virtualenv if it exists, rather than creating a new one every time
- `-p <version>`: use only the specified Python version, rather than repeating the operation for each supported Python version

For example:

```console
$ nox -rs tests -p 3.11
```

### Building documentation

```console
$ nox -s docs
```

### Checking type safety

```console
$ nox -s mypy
$ nox -s typeguard
```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_My Data Model_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@garethstockwell]'s [Hypermodern Python Cookiecutter] template.

[@garethstockwell]: https://github.com/garethstockwell
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/garethstockwell/cookiecutter-hypermodern-python
[file an issue]: https://github.com/garethstockwell/my-data-model/issues
[pip]: https://pip.pypa.io/
[attrs]: https://www.attrs.org/
[pydantic]: https://docs.pydantic.dev/
[pydantic-dataclasses]: https://docs.pydantic.dev/usage/dataclasses/

<!-- github-only -->

[license]: https://github.com/garethstockwell/my-data-model/blob/main/LICENSE
[contributor guide]: https://github.com/garethstockwell/my-data-model/blob/main/CONTRIBUTING.md
[command-line reference]: https://my-data-model.readthedocs.io/en/latest/usage.html
