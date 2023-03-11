"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """My Data Model."""


if __name__ == "__main__":
    main(prog_name="my-data-model")  # pragma: no cover
