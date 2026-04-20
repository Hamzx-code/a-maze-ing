from typing import Optional
from mazegen.Vec2 import Vec2
from config_validator.InvalidConfigException import InvalidConfigException

class InvalidConfigException(ValueError):
    """Exception raised when a maze configuration parameter is invalid."""

    def __init__(self, message: str = "Unspecified") -> None:
        """Initialize with a descriptive message.

        Args:
            message: Description of the invalid configuration.
                Defaults to ``"Unspecified"``.
        """
        super().__init__(f"Invalid Config: {message}")

class ConfigValidator:
    """Validate maze configuration parameters before generation."""

    @staticmethod
    def __validate_maze_dimensions(
        height: int,
        width: int,
        perfect: bool
    ) -> None:
        if not isinstance(height, int):
            raise InvalidConfigException(
                "Height must be an integer"
            )
        if not isinstance(width, int):
            raise InvalidConfigException(
                "Width must be an integer"
            )
        if not perfect and min(height, width) <= 1:
            raise InvalidConfigException(
                "Cannot generate an imperfect maze with width or height = 1"
            )
        if height < 1:
            raise InvalidConfigException(
                "Height must be >= 1"
            )
        if width < 1:
            raise InvalidConfigException(
                "Width must be >= 1"
            )

    @staticmethod
    def __validate_entry_exit(
        entry: Vec2,
        exit: Vec2,
        width: int,
        height: int,
    ) -> None:
        if not isinstance(entry, Vec2):
            raise InvalidConfigException(
                "Entry must be a Vec2 point"
            )
        if not isinstance(exit, Vec2):
            raise InvalidConfigException(
                "Exit must be a Vec2 point"
            )
        if entry.x == exit.x and entry.y == exit.y:
            raise InvalidConfigException(
                "Entry and exit must be different"
            )
        if not (0 <= entry.x < width):
            raise InvalidConfigException(
                "Entry.x must be >= 0 and < width"
            )
        if not (0 <= exit.x < width):
            raise InvalidConfigException(
                "Exit.x must be >= 0 and < width"
            )
        if not (0 <= entry.y < height):
            raise InvalidConfigException(
                "Entry.y must be >= 0 and < height"
            )
        if not (0 <= exit.y < height):
            raise InvalidConfigException(
                "Exit.y must be >= 0 and < height"
            )

    @staticmethod
    def __validate_perfect(perfect: bool) -> None:
        if type(perfect) is not bool:
            raise InvalidConfigException(
                "Perfect must be a boolean"
            )

    @staticmethod
    def __validate_output_file(output_file: str) -> None:
        if not isinstance(output_file, str):
            raise InvalidConfigException(
                "Output file must be a string"
            )
        if not len(output_file.strip()):
            raise InvalidConfigException(
                "Output file cannot be an empty string"
            )

    @staticmethod
    def __validate_seed(seed: Optional[str]) -> None:
        if seed is not None and not isinstance(seed, str):
            raise InvalidConfigException(
                "Seed must be None or a string"
            )
        if isinstance(seed, str) and not len(seed):
            raise InvalidConfigException(
                "Seed cannot be an empty string"
            )

    @classmethod
    def validate(
        cls,
        height: int,
        width: int,
        entry: Vec2,
        exit: Vec2,
        perfect: bool,
        output_file: str,
        seed: Optional[str]
    ) -> None:
        cls.__validate_maze_dimensions(
            height=height,
            width=width,
            perfect=perfect
        )
        cls.__validate_entry_exit(
            entry=entry,
            exit=exit,
            height=height,
            width=width
        )
        cls.__validate_perfect(perfect)
        cls.__validate_output_file(output_file)
        cls.__validate_seed(seed)
