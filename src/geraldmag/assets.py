"""
Asset management classes for GéraldMag.
"""

from pathlib import Path
from typing import Optional

import nanoid


class StyleCompiler:
    """
    Manages style compilation and aggregation.
    """

    def __init__(self):
        """Initialize the style compiler."""
        self._styles = []

    def add_style(self, path: Path, scope: Optional[str] = None) -> None:
        """
        Add a style file to be compiled.

        Args:
            path: Path to the style file (CSS or SCSS)
            scope: Optional scope to apply to the styles
        """
        pass

    def compile(self, output_path: Path):
        """
        Compile all registered styles into a single CSS file.

        Args:
            output_path: Path to write the compiled CSS
        """
        pass


class ImageBucket:
    """
    Manages image assets and their processing.
    """

    def __init__(self):
        """Initialize the image bucket."""
        self._images = {}

    def register_image(self, path: Path) -> str:
        """
        Register an image for processing and generate a unique ID.

        Args:
            path: Path to the image file

        Returns:
            Unique ID for the image
        """
        return nanoid.generate()

    def copy_images(self, output_dir: Path):
        """
        Copy all registered images to the output directory.

        Args:
            output_dir: Directory to copy images to
        """
        pass


class FontBucket:
    """
    Manages font assets and their processing.
    """

    def __init__(self):
        """Initialize the font bucket."""
        self._fonts = {}

    def register_font(self, path: Path):
        """
        Register a font for processing.

        Args:
            path: Path to the font file

        Returns:
            ID for the font
        """
        pass

    def copy_fonts(self, output_dir: Path):
        """
        Copy all registered fonts to the output directory.

        Args:
            output_dir: Directory to copy fonts to
        """
        pass
