#!/usr/bin/env python3

from mazegen import PrimGenerator, Vec2
from mazegen import GeneratorException
from src.parsing import parse, Parsed, ParseError
from src.visualizer import visualize
from pydantic import ValidationError
from pathlib import Path
import sys


def main(filename: str) -> None:
    """Parse the configuration file, generate a maze and launch the visualizer.

    Args:
        filename: Path to the configuration file to parse.
    """
    try:
        infos: Parsed = parse(filename)
    except ValidationError as e:
        print(e.errors()[0]["msg"])
        sys.exit(1)
    except (ParseError, OSError) as e:
        print(e)
        sys.exit(1)

    try:
        generator = PrimGenerator(
            infos.width,
            infos.height,
            Vec2(infos.entry[0], infos.entry[1]),
            Vec2(infos.exit[0], infos.exit[1]),
            seed=infos.seed,
            output_file=infos.output_file,
            is_perfect=infos.perfect,
            locked_cells=[
                [1, 0, 0, 0, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 0, 1, 1, 1],
                [0, 0, 1, 0, 1, 0, 0],
                [0, 0, 1, 0, 1, 1, 1],
            ]
        )
    except GeneratorException as e:
        print(f"An error occured during maze generation ({e})")
        sys.exit(1)

    try:
        visualize(generator)
    except GeneratorException as e:
        print(f"An error occured during maze generation ({e})")


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print(
                "Usage: python3 a_maze_ing.py [config_file] /",
                "make run /",
                "make run CONFIG=[config_file]"
            )
            sys.exit(1)
        path = Path(sys.argv[1])
        if path.suffix.lower() != ".txt":
            print("Error: configuration file must have a .txt extension")
            sys.exit(1)

        main(sys.argv[1])

    except Exception as e:
        print(f"an unexpected exception occured ({e})")
        sys.exit(1)
