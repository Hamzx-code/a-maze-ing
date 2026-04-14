
class ParseError(Exception):


    def __init__(self, msg: str = "Not specified") -> None:
        super().__init__(f"ParseError: {msg}")


