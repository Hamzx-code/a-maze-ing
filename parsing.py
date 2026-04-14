
class ParseError(Exception):


    def __init__(self, msg: str = "Not specified") -> None:
        super().__init__(f"ParseError: {msg}")


class Parsed(BaseModel):
    """
        width: Number of columns (>= 1).
        height: Number of rows (>= 1).
        entry: ``(x, y)`` coordinates of the maze entrance.
        exit: ``(x, y)`` coordinates of the maze exit.
        output_file: Path for the generated output.
        perfect: Whether the maze must be perfect (no loops).
        seed: RNG seed string.
    """

    width: int = Field(ge=1, le=200)
    height: int = Field(ge=1, le=200)
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str = Field(min_length=1)
    perfect: bool
    seed: Optional[str]

