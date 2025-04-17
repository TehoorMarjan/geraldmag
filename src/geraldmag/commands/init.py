import os
import shutil
from pathlib import Path

import click
import toml

from ..env import Environment


def init_project(force: bool = False):
    """
    Initialize a new GéraldMag project with default structure.

    Args:
        force: If True, overwrite existing files
    """
    # Check if the current directory already has GéraldMag files
    mag_toml_path = Path("mag.toml")

    # Get the path to the template directory
    template_dir = Path(__file__).parent.parent / "template"

    # Create the directory structure
    click.echo("Creating GéraldMag project structure...")

    # Create content directory and subdirectories
    os.makedirs("content/_default/styles", exist_ok=True)

    # Create mag.toml with default configuration using Environment
    env = Environment()
    default_config = env.dump_mandatory()

    if mag_toml_path.exists() and not force:
        click.echo(
            "Warning: mag.toml already exists, skipping this file. Use --force to overwrite."
        )
    else:
        with open(mag_toml_path, "w") as f:
            toml.dump(default_config, f)
        click.echo("Created mag.toml with default configuration.")

    # Create a default CSS file
    default_css_path = Path("content/_default/styles/main.css")
    css_template_path = template_dir / "init" / "main.css"
    
    if default_css_path.exists() and not force:
        click.echo(
            "Warning: Default CSS file already exists, skipping. Use --force to overwrite."
        )
    else:
        shutil.copy(css_template_path, default_css_path)
        click.echo("Created default CSS file.")

    # Create example README file
    readme_path = Path("README.md")
    readme_template_path = template_dir / "init" / "README.md"
    
    if readme_path.exists() and not force:
        click.echo(
            "Warning: README.md already exists, skipping. Use --force to overwrite."
        )
    else:
        shutil.copy(readme_template_path, readme_path)
        click.echo("Created README.md with basic instructions.")
        
    # Create .gitignore file
    gitignore_path = Path(".gitignore")
    gitignore_template_path = template_dir / "init" / "_gitignore"
    
    if gitignore_path.exists() and not force:
        click.echo(
            "Warning: .gitignore already exists, skipping. Use --force to overwrite."
        )
    else:
        shutil.copy(gitignore_template_path, gitignore_path)
        click.echo("Created .gitignore file.")

    click.echo(f"\n✅ GéraldMag project initialized successfully!")
    click.echo(f"\nNext steps:")
    click.echo(f"  1. Create a publication directory in content/")
    click.echo(f"  2. Add an index.html file to your publication")
    click.echo(f"  3. Run 'geraldmag new <publication-name>'")

    return True
