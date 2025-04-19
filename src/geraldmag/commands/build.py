"""
Build command for GéraldMag.
"""

from pathlib import Path

import click

from ..core import Builder
from ..env import Environment, EnvPath, PublicationEnvironment


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
    # Implementation will go here
    env = Environment.create()
    if verbose:
        env.verbose = True
    if output_path is not None:
        env.load({"output_path": output_path}, Path.cwd())
    # publication_name may either be a relative path or the name of a
    # publication inside env.content_dir
    pub_path = Path(publication_name)
    if pub_path.name == publication_name:
        # publication_name is the name of a publication inside env.content_dir
        pub_path = EnvPath(publication_name, env.content_dir.absolute)
        pub_name = publication_name
    else:
        # publication_name is a relative path
        pub_name = pub_path.name
        pub_path = EnvPath(publication_name)
    pub_env = PublicationEnvironment.from_env(
        env=env,
        publication_root=pub_path,
        publication_name=pub_name,
    )
    builder = Builder(env=pub_env)
    if clean:
        builder.clean()
    builder.build()
    click.echo(f"\n✅ Publication '{publication_name}' created successfully!")
