from prim import prim
from a_star import a_star
import time

width = 20
height = 20

NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000


def build_path_positions(start, path):
    x, y = start
    positions = [(x, y)]

    for move in path:
        if move == "N":
            y -= 1
        elif move == "S":
            y += 1
        elif move == "W":
            x -= 1
        elif move == "E":
            x += 1

        positions.append((x, y))

    return set(positions)


def display_maze_with_path(grid, width, height, start, end, path):
    RESET = "\033[0m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"

    path_positions = build_path_positions(start, path)

    for y in range(height):
        # haut des cellules
        for x in range(width):
            print("+", end="")
            if grid[y][x] & NORTH:
                print("---", end="")
            else:
                print("   ", end="")
        print("+")

        # milieu des cellules
        for x in range(width):
            if grid[y][x] & WEST:
                print("|", end="")
            else:
                print(" ", end="")

            if (x, y) == start:
                print(f"{BLUE} S {RESET}", end="")
            elif (x, y) == end:
                print(f"{YELLOW} E {RESET}", end="")
            elif (x, y) in path_positions:
                print(f"{GREEN} * {RESET}", end="")
            else:
                print("   ", end="")

        # mur droit
        if grid[y][width - 1] & EAST:
            print("|")
        else:
            print(" ")

    # bas du labyrinthe
    for x in range(width):
        print("+", end="")
        if grid[height - 1][x] & SOUTH:
            print("---", end="")
        else:
            print("   ", end="")
    print("+")


if __name__ == "__main__":

    grid = [[0xf] * width for _ in range(height)]

    start_time = time.perf_counter()
    prim(grid, width, height)
    prim_time = time.perf_counter() - start_time

    start_time = time.perf_counter()
    path1 = a_star(grid, (0, 0), (19, 19), width, height)
    a_star_time = time.perf_counter() - start_time

    display_maze_with_path(grid, width, height, (0, 0), (19, 19), path1)

    print(f"\nPrim time   : {prim_time:.6f} seconds")
    print(f"A* time     : {a_star_time:.6f} seconds")

    print("\n" * 3)


    grid1 = [[0xf] * width for _ in range(height)]

    start_time = time.perf_counter()
    prim(grid1, width, height, False, 0.1)
    prim_time2 = time.perf_counter() - start_time

    start_time = time.perf_counter()
    path2 = a_star(grid1, (0, 0), (19, 19), width, height)
    a_star_time2 = time.perf_counter() - start_time

    display_maze_with_path(grid1, width, height, (0, 0), (19, 19), path2)

    print(f"\nPrim time 2 : {prim_time2:.6f} seconds")
    print(f"A* time 2   : {a_star_time2:.6f} seconds")
