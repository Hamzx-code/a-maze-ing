from enum import IntFlag


class EDirection(IntFlag):
    """
        NORTH = 1   or 0001
        EAST = 2    or 0010
        SOUTH = 4   or 0100
        WEST = 8    or 1000
    """

    NORTH = 1 << 0
    EAST = 1 << 1
    SOUTH = 1 << 2
    WEST = 1 << 3
    ALL = 15
