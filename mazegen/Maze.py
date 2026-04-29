from mazegen.Cell import Cell
from mazegen.GeneratorException import GeneratorException
from mazegen.Vec2 import Vec2
from mazegen.Direction import EDirection
from enum import IntEnum, auto
from typing import Dict, List, Literal, Optional, Tuple
from sortedcontainers import SortedKeyList

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


