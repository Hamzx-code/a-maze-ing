from mazegen.Cell import Cell
from mazegen.GeneratorException import GeneratorException
from mazegen.Vec2 import Vec2
from mazegen.Direction import EDirection
from enum import IntEnum, auto
from typing import Dict, List, Literal, Optional, Tuple

Coord = Tuple[int, int]


class Maze:
    """
    The maze
    """

    class Status(IntEnum):
        """ Lifcycle of the maze """

        BLANK = auto()
        INITIALIZED = auto()
        GENERATING = auto()
        GENERATED = auto()
        SOLVED = auto()

    map: List[List[Cell]]
    width: int
    height: int
    status: "Maze.Status"
    start_pos: Vec2
    end_pos: Vec2
    locked_cells: List[Cell]
    add_ft_pattern: bool
    solution: List[Coord]

    def __init__(self) -> None:
        """Initialize an empty maze
        with status 'BLANK'"""
        self.map: List[List[Cell]] = []
        self.height = 0
        self.width = 0
        self.status = Maze.Status.BLANK
        self.start_pos = Vec2(0, 0)
        self.end_pos = Vec2(0, 0)
        self.locked_cells = []
        self.ft_pattern_end = Vec2(0, 0)
        self.add_ft_pattern = False
        self.solution = []

    def reset_map(self) -> None:
        """Reset every cell and set status to 'BLANK'"""
        self.status = Maze.Status.BLANK
        for line in self.map:
            for cell in line:
                cell.reset_cell()

    def init_map(
        self,
        width: int,
        height: int,
        start_pos: Vec2,
        end_pos: Vec2,
        locked_cells: Optional[List[List[Literal[0, 1]]]] = None
    ) -> None:
        """
        Locked cells can't be carved
        """
        self.status = Maze.Status.INITIALIZED
        self.width = width
        self.height = height
        self.start_pos = start_pos
        self.end_pos = end_pos

        # Init the map as a list of list of cells
        self.map = [
            [Cell(position=Vec2(x, y)) for x in range(width)]
            for y in range(height)
        ]

        if locked_cells is None:
            return

        locked_cells_height = len(locked_cells)
        locked_cells_width = len(locked_cells[0])

        if (
            height >= locked_cells_height + 1
            and width >= locked_cells_width + 1
        ):

            locked_cells_y = int(height / 2 - (locked_cells_height) / 2)
            locked_cells_x = int(width / 2 - (locked_cells_width) / 2)

            for y in range(locked_cells_height):
                for x in range(locked_cells_width):
                    n_x = locked_cells_x + x
                    n_y = locked_cells_y + y
                    self.map[n_y][n_x].locked = locked_cells[y][x] == 1
                    if locked_cells[y][x] == 1 and Vec2(n_x, n_y) in [
                        self.start_pos,
                        self.end_pos,
                    ]:
                        raise GeneratorException(
                            "Entry or exit cannot be in the locked" +
                            " cells pattern"
                        )
        else:
            print(
                "Cannot place the 42 pattern,",
                "will generate the maze without it."
            )

    def carve_cell(self, cell: Cell, directions: int) -> None:
        if cell.locked:
            raise GeneratorException("Cannot carve a locked cell")

        if directions & EDirection.NORTH.value:
            if cell.position.y <= 0:
                raise GeneratorException(
                    "Cannot carve a cell with y = 0 to the north"
                )
            self.map[cell.position.y - 1][cell.position.x].carve(
                EDirection.SOUTH
            )
            cell.carve(EDirection.NORTH)

        if directions & EDirection.EAST.value:
            if cell.position.x >= self.width - 1:
                raise GeneratorException(
                    "Cannot carve a cell with x = width - 1 to the east"
                )
            self.map[cell.position.y][cell.position.x + 1].carve(
                EDirection.WEST
            )
            cell.carve(EDirection.EAST)

        if directions & EDirection.SOUTH.value:
            if cell.position.y >= self.height - 1:
                raise GeneratorException(
                    "Cannot carve a cell with y = height - 1 to the south"
                )
            self.map[cell.position.y + 1][cell.position.x].carve(
                EDirection.NORTH
            )
            cell.carve(EDirection.SOUTH)

        if directions & EDirection.WEST.value:
            if cell.position.x <= 0:
                raise GeneratorException(
                    "Cannot carve a cell with x = 0 to the west"
                )
            self.map[cell.position.y][cell.position.x - 1].carve(
                EDirection.EAST
            )
            cell.carve(EDirection.WEST)

    def solve(self) -> None:
        """Find the shortest path from start to end using A*.

        Results are stored in :attr:`solution` as a list of
        ``(x, y)`` coordinate tuples ordered from start to end.
        Sets :attr:`status` to ``SOLVED`` if a path is found.
        """
        from heapq import heappush, heappop

        start: Coord = (self.start_pos.x, self.start_pos.y)
        end: Coord = (self.end_pos.x, self.end_pos.y)
        directions: List[EDirection] = [
            EDirection.NORTH,
            EDirection.EAST,
            EDirection.SOUTH,
            EDirection.WEST,
        ]
        moves: Dict[EDirection, Coord] = {
            EDirection.NORTH: (0, -1),
            EDirection.EAST:  (1, 0),
            EDirection.SOUTH: (0, 1),
            EDirection.WEST:  (-1, 0),
        }

        def heuristic(pos: Coord) -> int:
            """Manhattan distance from *pos* to the exit."""
            return abs(end[0] - pos[0]) + abs(end[1] - pos[1])

        # Min-heap entries: (f_score, g_score, position)
        open_list: List[Tuple[int, int, Coord]] = []
        heappush(open_list, (heuristic(start), 0, start))
        came_from: Dict[Coord, Coord] = {}
        g_score: Dict[Coord, int] = {start: 0}

        while open_list:
            _, g, current = heappop(open_list)

            # Stale entry: a better path to this cell was already found
            if g > g_score.get(current, float('inf')):
                continue

            if current == end:
                # Reconstruct path from end back to start
                path: List[Coord] = []
                cursor: Coord = current
                while cursor in came_from:
                    path.append(cursor)
                    cursor = came_from[cursor]
                path.append(start)
                path.reverse()
                self.solution = path
                self.status = Maze.Status.SOLVED
                return

            x, y = current
            curr_cell: Cell = self.map[y][x]
            for direction in directions:
                # Skip if there is a wall in this direction
                if curr_cell.walls & direction.value:
                    continue
                move_x, move_y = moves[direction]
                neighbour: Coord = (x + move_x, y + move_y)
                g_new: int = g + 1
                if g_new < g_score.get(neighbour, float('inf')):
                    g_score[neighbour] = g_new
                    f: int = g_new + heuristic(neighbour)
                    came_from[neighbour] = current
                    heappush(open_list, (f, g_new, neighbour))
        # No path found
        self.solution = []
