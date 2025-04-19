import click

from .commands.build import build_process
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


@cli.command("build")
@click.argument("publication_name")
@click.option("--verbose", is_flag=True, help="Show detailed logging")
@click.option(
    "--clean", is_flag=True, help="Clean output directories before building"
)
@click.option(
    "--output-path",
    type=click.Path(exists=False, file_okay=False, path_type=str),
    help="Custom output path for the PDF",
)
def build(
    publication_name: str,
    clean: bool = False,
    output_path: str | None = None,
    verbose: bool = False,
):
    """Initialize a new GéraldMag project."""
    build_process(
        publication_name=publication_name,
        clean=clean,
        output_path=output_path,
        verbose=verbose,
    )


def main():
    cli()


if __name__ == "__main__":
    main()
