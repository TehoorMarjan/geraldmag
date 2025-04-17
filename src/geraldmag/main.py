import click

from .commands.init import init_project
from .commands.new import create_publication


@click.group()
@click.version_option()
def cli():
    """GéraldMag - Create complex documents with WeasyPrint."""
    pass


@cli.command("init")
@click.option("--force", is_flag=True, help="Overwrite existing files")
def init(force: bool):
    """Initialize a new GéraldMag project."""
    init_project(force)


@cli.command("new")
@click.argument("publication_name")
@click.option("--force", is_flag=True, help="Overwrite existing publication")
def new(publication_name: str, force: bool):
    """Create a new publication."""
    create_publication(publication_name, force)


def main():
    cli()


if __name__ == "__main__":
    main()
