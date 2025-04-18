"""
Type definitions for GéraldMag processors.
"""

from pathlib import Path
from typing import Protocol

from ..core import PageContext


class PProcessor(Protocol):
    """
    Protocol defining the interface for content processors.
    """

    def process(self, file_path: Path, context: PageContext) -> str:
        """
        Process a file and return the processed content.

        Args:
            file_path: Path to the file to process
            context: Page context for the processing

        Returns:
            Processed content as string
        """
        ...
