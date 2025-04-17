"""
Configuration environment for GéraldMag.
"""

import functools
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, get_origin, get_type_hints

import toml

type Mandatory[T] = T


@dataclass(frozen=True)
class EnvPath:
    """
    A special type for handling paths in the Environment.

    EnvPath maintains both the raw path (as specified by the user) and the
    absolute path (resolved against a reference directory).
    """

    value: str
    setfrom: Path = field(default_factory=Path.cwd)

    @functools.cached_property
    def absolute(self) -> Path:
        """Return the absolute path resolved against the reference directory."""
        return (self.setfrom / self.value).absolute().resolve()

    def __str__(self) -> str:
        """String representation returns the raw path."""
        return self.value


@dataclass
class Environment:
    """
    Configuration environment for GéraldMag.

    The Environment class manages configuration parameters with default values,
    mandatory fields, and methods for loading/dumping configuration.

    This class is designed to be extended with cascading environments
    (app → publication → article).
    """

    # Mandatory fields (require a value in mag.toml)
    title: Mandatory[str] = "My GéraldMag Publication"

    # Optional fields with sane defaults - these are all paths
    content_dir: EnvPath = field(default_factory=lambda: EnvPath("content"))
    default_dir: EnvPath = field(
        default_factory=lambda: EnvPath("content/_default")
    )
    resources_dir: EnvPath = field(
        default_factory=lambda: EnvPath("_resources")
    )
    output_dir: EnvPath = field(default_factory=lambda: EnvPath("out"))

    def load(self, config_dict: Dict[str, Any], config_path: Path) -> None:
        """
        Load configuration from a dictionary and update instance attributes.

        Args:
            config_dict: Dictionary containing configuration values
            config_path: Path to the directory containing the config file
        """
        # Get type hints for all fields
        hints = get_type_hints(self.__class__, include_extras=True)

        for key, value in config_dict.items():
            if hasattr(self, key):
                # Check if the attribute is a path type
                if key in hints and get_origin(hints[key]) == EnvPath:
                    # Create EnvPath with the raw value and reference directory
                    setattr(
                        self, key, EnvPath(value=value, setfrom=config_path)
                    )
                else:
                    # For non-path types, just set the value directly
                    setattr(self, key, value)

    def dump_mandatory(self) -> Dict[str, Any]:
        """
        Return a dictionary containing only the mandatory parameters with their default values.

        Returns:
            Dictionary with mandatory parameters
        """
        return {
            key: value
            for key, value in self.__dict__.items()
            if key in self.__annotations__
            and self.__annotations__[key].__name__ == "Mandatory"
        }

    @classmethod
    def create(cls, config_path: str = "mag.toml") -> "Environment":
        """
        Create an Environment instance by loading from mag.toml if it exists.

        Args:
            config_path: Path to the configuration file (default: mag.toml)

        Returns:
            Configured Environment instance
        """
        env = cls()

        # Load config file if it exists
        config_file = Path(config_path).absolute().resolve()
        if config_file.exists():
            try:
                config = toml.load(config_file)
                env.load(config, config_file.parent)
            except Exception as e:
                print(f"Warning: Error loading configuration file: {e}")

        return env
