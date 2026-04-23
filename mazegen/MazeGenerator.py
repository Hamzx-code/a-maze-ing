from mazegen.Vec2 import Vec2
from mazegen.Cell import Cell
from typing import Literal, Optional, Union, List
from abc import ABC, abstractmethod
from random import Random
from config_validatior import ConfigValidator

class MazeGenerator(ABC):
    __maze: Maze
    __seed: Union[str, None]
    __rng: Random
    __height: int
    __width: int
    __start_pos: Vec2
    __end_pos: Vec2
    __output_file: str
    __locked_cells: Optional[List[List[Literal[0, 1]]]]

    """
        width: Number of columns in the maze.
        height: Number of rows in the maze.
        start_pos: Entry point of the maze.
        end_pos: Exit point of the maze.
        seed: Optional RNG seed for reproducible generation.
        add_ft_pattern: Whether to overlay the 42 pattern onto the maze.
        is_perfect: Whether the maze should be perfect.
        output_file: Path to the file where the maze will be written.
    """
    def __init__(
        self,
        width: int,
        height: int,
        start_pos: Vec2,
        end_pos: Vec2,
        seed: Optional[str] = None,
        locked_cells: Optional[List[List[Literal[0, 1]]]] = None,
        is_perfect: bool = True,
        output_file: str = "output_maze.txt",
    ) -> None:
 
        ConfigValidator.validate(
            height=height,
            width=width,
            entry=start_pos,
            exit=end_pos,
            seed=seed,
            perfect=is_perfect,
            output_file=output_file
        )
        self.__seed = seed
        self.__rng = Random(seed)
        self.__maze = Maze()
        self.__width = width
        self.__height = height
        self.__start_pos = start_pos
        self.__end_pos = end_pos
        self.__locked_cells = locked_cells
        self.__maze.init_map(width, height, start_pos, end_pos, locked_cells)
        self.__is_perfect = is_perfect
        self.__output_file = output_file

