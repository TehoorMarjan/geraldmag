"""
Template engine for GéraldMag.
"""

from pathlib import Path

import jinja2

from .core import Context, PageContext
from .processors import ProcessorFactory


class Engine:
    """
    Template engine that processes content using Jinja2.
    """

    def __init__(self, context: Context):
        """
        Initialize the template engine.

        Args:
            context: Context for the build process
        """
        self.context = context
        self.processor_factory = ProcessorFactory()

        # Setup Jinja environment with custom functions
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                str(context.env.content_dir.absolute)
            ),
            autoescape=jinja2.select_autoescape(["html", "xml"]),
        )

        # Register custom functions
        self._register_jinja_functions()

    def process(self, template_path: Path) -> str:
        """
        Process a template file.

        Args:
            template_path: Path to the template file

        Returns:
            Processed template content
        """
        # Convert absolute path to relative path based on content_dir
        rel_path = template_path.relative_to(
            self.context.env.content_dir.absolute
        )

        # Get the template
        template = self.env.get_template(str(rel_path))

        # Render the template with the context
        return template.render(context=self.context)

    def _register_jinja_functions(self) -> None:
        """
        Register custom functions with the Jinja environment.
        """

        # Function to include a content file (either md or html)
        def include_content(file_path: str) -> str:
            # Convert to absolute path
            content_dir = self.context.env.content_dir.absolute
            if Path(file_path).is_absolute():
                abs_path = Path(file_path)
            else:
                abs_path = content_dir / file_path

            page_context = PageContext(self.context)

            # Get the appropriate processor
            processor = self.processor_factory.get_processor(abs_path)

            # Process the content
            return processor().process(abs_path, page_context)

        # Register the function
        self.env.globals["include_content"] = include_content  # type: ignore
