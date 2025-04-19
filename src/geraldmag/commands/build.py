"""
Build command for GéraldMag.
"""

from pathlib import Path

import click

from ..builder import Builder
from ..env import EnvPath, PublicationEnvironment


def build_process(
    publication_name: str,
    clean: bool = False,
    output_path: str | None = None,
    verbose: bool = False,
):
    """
    Build a publication into a PDF.

    Args:
        publication_name: Name of the publication to build
        clean: If True, clean output directories before building
        output_path: Optional custom output path for the PDF
        verbose: If True, show detailed logging
    """
    # publication_name may either be a relative path or the name of a
    # publication inside env.content_dir
    pub_path = Path(publication_name)
    # Initialise like publication_name is a relative path
    env = PublicationEnvironment.create(
        publication_root=EnvPath(publication_name),
        publication_name=pub_path.name,
    )
    # If finally, publication_name is not a relative path, change environment
    if pub_path.name == publication_name:
        # publication_name is the name of a publication inside env.content_dir
        env.publication_root = EnvPath(
            publication_name, env.content_dir.absolute
        )
    if verbose:
        env.verbose = True
    if output_path is not None:
        env.load({"output_path": output_path}, Path.cwd())
    builder = Builder(env=env)
    if clean:
        builder.clean()
    builder.build()
    click.echo(f"\n✅ Publication '{publication_name}' created successfully!")
