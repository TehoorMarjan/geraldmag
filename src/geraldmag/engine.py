"""
Template engine for GéraldMag.
"""

from pathlib import Path
from typing import Optional, Type, cast

import jinja2
from jinja2 import Environment, nodes
from jinja2.ext import Extension
from jinja2.parser import Parser

from .context import Context, PageContext
from .processors import ProcessorFactory


class ContentExtension(Extension):
    """
    Jinja2 extension that adds a {% content 'path/to/file.md' %} tag
    which processes and includes content files (md, html).
    """

    tags = {"content"}

    def __init__(self, environment: Environment) -> None:
        super().__init__(environment)
        self.context: Optional[Context] = None
        self.processor_factory: Optional[ProcessorFactory] = None

    def set_context(
        self, context: Context, processor_factory: ProcessorFactory
    ) -> None:
        """Set the context and processor factory for the extension."""
        self.context = context
        self.processor_factory = processor_factory

    def parse(self, parser: Parser) -> nodes.Node:
        """Parse the content tag."""
        lineno = next(parser.stream).lineno

        # Parse the file path argument
        file_path = parser.parse_expression()

        # Create a call to _render_content with the file path
        call = self.call_method("_render_content", [file_path], lineno=lineno)

        # Return the output node that will render the content
        return nodes.Output([nodes.MarkSafe(call)]).set_lineno(lineno)

    def _render_content(self, file_path: str) -> str:
        """
        Process and render a content file.

        Args:
            file_path: Path to the content file

        Returns:
            Processed content
        """
        if not self.context or not self.processor_factory:
            raise RuntimeError(
                "ContentExtension not properly initialized with context and processor factory"
            )

        # Convert to absolute path
        content_dir = self.context.env.content_dir.absolute
        if Path(file_path).is_absolute():
            abs_path = Path(file_path)
        else:
            abs_path = content_dir / file_path

        page_context = PageContext(self.context)

        # Get the appropriate processor
        processor_cls = self.processor_factory.get_processor(abs_path)

        # Process the content and return it as a string
        return processor_cls().process(abs_path, page_context)


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

        # Create our custom extension instance
        self.content_extension: Type[ContentExtension] = ContentExtension

        # Setup Jinja environment with our custom extension
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                str(context.env.content_dir.absolute)
            ),
            autoescape=jinja2.select_autoescape(["html", "xml"]),
            extensions=[self.content_extension],
        )

        # Initialize our extension with the context
        ext = cast(
            ContentExtension,
            self.env.extensions[self.content_extension.identifier],
        )
        ext.set_context(context, self.processor_factory)

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
