import random
from enum import Enum
from typing import Any, Dict, List, Tuple, Union
from mlx import Mlx
from pynput import keyboard
from pynput.keyboard import Key, KeyCode
from mazegen import MazeGenerator
from mazegen.Cell import Cell
from mazegen.Direction import EDirection


class EWalls(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


WALL_WIDTH_RATIO: float = 0.25
Color = Tuple[int, int, int, int]
WallInfo = Tuple[Tuple[int, int], EWalls]

class Visualizer:
