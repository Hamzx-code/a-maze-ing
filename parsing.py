
class ParseError(Exception):
    """Raised when the configuration file is malformed.

    Args:
        msg: Human-readable description of the problem.
    """

    def __init__(self, msg: str = "Not specified") -> None:
        """Initialize with a prefixed error message.

        Args:
            msg: Description of the parse error.
                Defaults to ``"Not specified"``.
        """
        super().__init__(f"ParseError: {msg}")


