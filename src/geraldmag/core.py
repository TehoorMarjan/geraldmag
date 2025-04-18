"""
Core classes for GéraldMag.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import nanoid

from .assets import FontBucket, ImageBucket, StyleCompiler
from .engine import Engine
from .env import Environment


@dataclass
class Context:
    """
    Context object that holds the state of the build process.
    
    Args:
        env: Environment configuration
        publication: Name of the publication
    """
    env: Environment
    publication: str
    styles: StyleCompiler = field(default_factory=StyleCompiler)
    images: ImageBucket = field(default_factory=ImageBucket)
    fonts: FontBucket = field(default_factory=FontBucket)


class PageContext(Context):
    """
    Context for a specific page in the publication.
    """

    def __init__(self, parent_context: Context):
        """
        Initialize a new PageContext from a parent Context.

        Args:
            parent_context: Parent context to inherit from
        """
        self.env = parent_context.env
        self.publication = parent_context.publication
        self.styles = parent_context.styles
        self.images = parent_context.images
        self.fonts = parent_context.fonts
        self.scope = nanoid.generate()
        self.page: Dict[str, Any] = {}
        self.content: str = ""


class Builder:
    """
    Manages the build process for a publication.
    """

    def __init__(self, publication_name: str, env: Environment):
        """
        Initialize a new Builder.

        Args:
            publication_name: Name of the publication to build
            env: Environment configuration
        """
        self.publication_name = publication_name
        self.env = env
        self.context = Context(env, publication_name)
        self.engine = Engine(self.context)

    def build(self, clean: bool = False, output_path: Optional[str] = None):
        """
        Build the publication into a PDF.

        Args:
            clean: If True, clean output directories before building
            output_path: Optional custom output path for the PDF

        Returns:
            Path to the generated PDF file
        """
        # Build process steps
        self._build_html()
        self._compile_scss()
        self._generate_pdf(output_path)

    def _build_html(self):
        """
        Build the HTML structure from the publication content.
        """
        pass

    def _compile_scss(self):
        """
        Compile SCSS files to CSS.
        """
        pass

    def _generate_pdf(
        self,
        output_path: Optional[str] = None,
    ):
        """
        Generate the PDF from HTML and CSS.

        Args:
            output_path: Optional custom output path for the PDF
        """
        pass
