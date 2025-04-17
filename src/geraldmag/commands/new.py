"""
Command to create a new publication in a GéraldMag project.
"""
import os
import shutil
from pathlib import Path

import click

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
    
    # Get the template directory
    template_dir = Path(__file__).parent.parent / "template" / "skeleton"
    
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
    os.makedirs(publication_dir, exist_ok=True)
    
    # Copy the skeleton template to the publication directory
    for item in template_dir.glob('*'):
        if item.is_dir():
            # For directories, copy recursively
            dst_dir = publication_dir / item.name
            if dst_dir.exists() and force:
                shutil.rmtree(dst_dir)
            
            if not dst_dir.exists():
                shutil.copytree(item, dst_dir)
                click.echo(f"Created {item.name}/ directory.")
        else:
            # For files, copy directly
            dst_file = publication_dir / item.name
            if not dst_file.exists() or force:
                shutil.copy2(item, dst_file)
                click.echo(f"Created {item.name} file.")
    
    click.echo(f"\n✅ Publication '{publication_name}' created successfully!")
    click.echo(f"\nNext steps:")
    click.echo(f"  1. Edit the index.html file in {publication_dir}")
    click.echo(f"  2. Add articles to the {publication_dir}/articles directory")
    click.echo(f"  3. Run 'geraldmag build {publication_name}' to generate your PDF")
    
    return True