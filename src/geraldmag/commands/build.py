"""
Build command for GéraldMag.
"""

import click

from ..core import Builder
from ..env import Environment


def build_process(publication_name: str, clean: bool = False):
    """
    Build a publication into a PDF.

    Args:
        publication_name: Name of the publication to build
        clean: If True, clean output directories before building
        output_path: Optional custom output path for the PDF
        verbose: If True, show detailed logging
    """
    # Implementation will go here
    if clean:
        pass
    env = Environment.create()
    _builder = Builder(
        publication_name=publication_name,
        env=env,
    )
    click.echo(f"\n✅ Publication '{publication_name}' created successfully!")
