#!/usr/bin/env python3

from mazegen import Vec2
from src.parsing import parse, Parsed, ParseError
from pydantic import ValidationError
import sys


def main(filename: str) -> None:
    """
    Parse the config file
    Generate a maze
    Launch the visualizer
    """
    try:
        infos: Parsed = parse(filename)
    except ValidationError as e:
        print(e.errors()[0]["msg"])
        sys.exit(1)
    except (ParseError, OSError) as e:
        print(e)
        sys.exit(1)
    print(infos)



if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print(
                "Usage: python3 a_maze_ing.py [config_file] /",
                "make run /",
                "make run CONFIG=[config_file]"
            )
            sys.exit(1)

        main(sys.argv[1])

    except Exception as e:
        print(f"an unexpected exception occured ({e})")
        sys.exit(1)
