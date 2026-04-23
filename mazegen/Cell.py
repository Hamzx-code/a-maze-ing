from mazegen.Direction import EDirection
from mazegen.Vec2 import Vec2


class Cell:
    """
    A single cell in the maze grid.
    Walls are stored as a 'Direction' bitmask,
    each bits represent a wall of the cell.
        position: Grid coordinates of this cell.
        walls: Bitmask of current walls. Defaults to 'EDirection.ALL'
        (every wall are present).
        locked: If 'True', the cell cannot be carved or modified.
    """

    position: Vec2
    locked: bool
    walls: int

    def __init__(
        self,
        position: Vec2,
        walls: int = EDirection.ALL.value,
        locked: bool = False,
    ):
        """
        Position in the maze
        The bits that represents the differents walls of the cells
        True or False depends on the state of the Cell
        """
        self.position = position
        self.walls = walls
        self.locked = locked

    def carve(self, direction: EDirection) -> None:
        """
        Carve the wall of a cell in a given direction
        """
        if self.locked:
            raise GeneratorException("Cannot edit a locked cell")
        if self.walls & direction.value:
            self.walls -= direction.value

    def reset_cell(self) -> None:
        """Restore all walls and unlock the cell."""
        self.walls = EDirection.ALL.value
        self.locked = False
