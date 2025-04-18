"""
Processor factory for content processing.
"""

from pathlib import Path
from typing import Dict, Type

from .html import HTMLProcessor
from .markdown import MarkdownProcessor
from .types import PProcessor


class ProcessorFactory:
    """
    Factory for creating content processors based on file type.
    """

    PROCESSORS: Dict[str, Type[PProcessor]] = {
        ".md": MarkdownProcessor,
        ".html": HTMLProcessor,
    }

    @classmethod
    def get_processor(cls, file_path: Path) -> Type[PProcessor]:
        """
        Get an appropriate processor for the given file.

        Args:
            file_path: Path to the file to process

        Returns:
            A processor instance for the file type

        Raises:
            ValueError: If no processor is available for the file type
        """
        suffix = file_path.suffix.lower()
        processor_cls = cls.PROCESSORS.get(suffix)

        if processor_cls is None:
            raise ValueError(f"No processor available for file type: {suffix}")

        return processor_cls
