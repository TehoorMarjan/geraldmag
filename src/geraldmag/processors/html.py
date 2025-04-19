"""
HTML processor for GéraldMag.
"""

from pathlib import Path

from ..context import PageContext


class HTMLProcessor:
    """
    Processor for HTML content files.
    """

    def process(self, file_path: Path, context: PageContext) -> str:
        """
        Process an HTML file and return the processed content.

        Args:
            file_path: Path to the HTML file
            context: Page context for the processing

        Returns:
            Processed HTML content
        """
        # Read the content
        html_content = file_path.read_text(encoding="utf-8")

        # Check for associated style files
        self._add_styles(file_path, context)

        # Process the content as a template if needed
        # (this will be handled by the Engine class)

        return html_content

    def _add_styles(self, file_path: Path, context: PageContext) -> None:
        """
        Add any styles associated with this HTML file to the context.

        Args:
            file_path: Path to the HTML file
            context: Page context
        """
        # Check for CSS or SCSS file with the same name
        base_path = file_path.with_suffix("")

        css_path = base_path.with_suffix(".css")
        if css_path.exists():
            context.styles.add_style(css_path, context.scope)

        scss_path = base_path.with_suffix(".scss")
        if scss_path.exists():
            context.styles.add_style(scss_path, context.scope)

        # Also check for style.css or style.scss in the same directory
        dir_path = file_path.parent

        css_path = dir_path / "style.css"
        if css_path.exists():
            context.styles.add_style(css_path, context.scope)

        scss_path = dir_path / "style.scss"
        if scss_path.exists():
            context.styles.add_style(scss_path, context.scope)
