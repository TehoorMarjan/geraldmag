"""
Markdown processor for GéraldMag.
"""

from pathlib import Path
from typing import Any

import frontmatter  # type: ignore
import markdown

from ..context import PageContext


class MarkdownProcessor:
    """
    Processor for Markdown content files.
    """

    def process(self, file_path: Path, context: PageContext) -> str:
        """
        Process a Markdown file and return HTML.

        Args:
            file_path: Path to the Markdown file to process
            context: Page context for the processing

        Returns:
            Processed HTML content
        """
        # Extract frontmatter and Markdown content
        frontmatter_data, content = self._get_frontmatter(file_path)

        # Update context with frontmatter
        context.page = frontmatter_data

        # Convert Markdown to HTML
        html_content = self._markdown_to_html(content)
        context.content = html_content

        # Process any style file referenced in frontmatter
        if "style" in context.page:
            style_path = file_path.parent / context.page["style"]
            if style_path.exists():
                context.styles.add_style(style_path, context.scope)

        # Apply template to content
        result = self._make_article(context)
        return result

    def _get_frontmatter(self, file_path: Path) -> tuple[dict[str, Any], str]:
        """
        Extract frontmatter from a Markdown file.

        Args:
            file_path: Path to the Markdown file

        Returns:
            Tuple of frontmatter data and Markdown content
        """
        with file_path.open("r", encoding="utf-8") as f:
            metadata, content = frontmatter.parse(f.read())
        return metadata, content

    def _markdown_to_html(self, content: str) -> str:
        """
        Convert Markdown content to HTML.

        Args:
            content: Markdown content

        Returns:
            HTML content
        """
        return markdown.markdown(
            content, extensions=["fenced_code", "codehilite"]
        )

    def _make_article(self, context: PageContext) -> str:
        """
        Apply template to the article content.

        Args:
            context: Page context with content and frontmatter

        Returns:
            Final HTML for the article
        """
        return ""
