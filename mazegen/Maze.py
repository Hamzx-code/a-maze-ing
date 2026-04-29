from mazegen.Cell import Cell
from mazegen.GeneratorException import GeneratorException
from mazegen.Vec2 import Vec2
from mazegen.Direction import EDirection
from enum import IntEnum, auto
from typing import Dict, List, Literal, Optional, Tuple
from sortedcontainers import SortedKeyList

Coord = Tuple[int, int]

class Maze:

    class Status(IntEnum):
    """ Lifcycle of the maze """
        BLANK = auto()
        INITIALIZED = auto()
        GENERATING = auto()
        GENERATED = auto()
        SOLVED = auto()


    def __init__(self) -> None:

    def reset_map(self) -> None:

