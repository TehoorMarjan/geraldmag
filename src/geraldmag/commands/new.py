"""
Command to create a new publication in a GéraldMag project.
"""

import importlib.resources
import shutil
from importlib.abc import Traversable
from pathlib import Path

import click

from .. import templates
from ..env import Environment


def create_publication(publication_name: str, force: bool = False):
    """
    Create a new publication with the given name.

    Args:
        publication_name: Name of the publication to create
        force: If True, overwrite existing files
    """
    # Load environment from mag.toml
    env = Environment.create()

    # Get the template directory using importlib.resources
    templates_path = importlib.resources.files(templates)
    skeleton_dir = templates_path.joinpath("skeleton")

    # Create the publication directory path
    content_dir_path = env.content_dir.absolute
    publication_dir = content_dir_path / publication_name

    # Check if publication directory already exists
    if publication_dir.exists():
        if not force:
            click.echo(f"Publication '{publication_name}' already exists.")
            click.echo(f"Use --force to overwrite.")
            return False

    # Create the publication directory
    click.echo(f"Creating new publication: {publication_name}")
    publication_dir.mkdir(parents=True, exist_ok=True)

    # Copy the skeleton directory structure to the new publication directory
    # Use a function so we can leverage recursion
    def copy_dir(src: Traversable, dst: Path):
        dst.mkdir(parents=True, exist_ok=True)
        for item in src.iterdir():
            if item.is_dir():
                copy_dir(item, dst / item.name)
            else:
                with item.open("rb") as src_file:
                    with (dst / item.name).open("wb") as dst_file:
                        shutil.copyfileobj(src_file, dst_file)

    copy_dir(skeleton_dir, publication_dir)

    click.echo(f"\n✅ Publication '{publication_name}' created successfully!")
    click.echo(f"\nNext steps:")
    click.echo(f"  1. Edit the index.html file in {publication_dir}")
    click.echo(
        f"  2. Add articles to the {publication_dir}/articles directory"
    )
    click.echo(
        f"  3. Run 'geraldmag build {publication_name}' to generate your PDF"
    )

    return True
