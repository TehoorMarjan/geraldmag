"""
Context classes for GéraldMag.
"""

from dataclasses import dataclass, field
from typing import Any, Dict

import nanoid

from .assets import FontBucket, ImageBucket, StyleCompiler
from .env import PublicationEnvironment


@dataclass
class Context:
    """
    Context object that holds the state of the build process.

    Args:
        env: Environment configuration
        publication: Name of the publication
    """

    env: PublicationEnvironment
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
