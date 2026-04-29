# ************************************************************************** #
#                                                                            #
#                                                        :::      ::::::::   #
#   prim.py                                            :+:      :+:    :+:   #
#                                                    +:+ +:+         +:+     #
#   By: hhamidi <hhamidi@student.42lyon.fr>        +#+  +:+       +#+        #
#                                                +#+#+#+#+#+   +#+           #
#   Created: 2026/04/29 17:08:28 by hhamidi           #+#    #+#             #
#   Updated: 2026/04/29 17:08:28 by hhamidi          ###   ########.fr       #
#                                                                            #
# ************************************************************************** #

from random import randint, choice, randrange, random
from time import time
from prim_utils import get_unvisited_neighbors, get_visited_neighbors
from prim_utils import remove_wall, would_create_3x3


width = 50
height = 50

NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000

grid = [[0xf] * width for _ in range(height)]


def prim(grid: list[list[int]], width: int, height: int,
              perfect: bool = True, imperfection_rate: float = 0.1) -> None:

    frontiers: list[tuple[int, int]] = []
    visited_cells: set[tuple[int, int]] = set()
    cell = (randint(0, width - 1), randint(0, height - 1))

    visited_cells.add(cell)

    get_unvisited_neighbors(frontiers, visited_cells, cell, width,
                            height)
    while frontiers:
        visited_neighbors: list[tuple[int, int]] = []
        idx = randrange(len(frontiers))
        random_cell = frontiers[idx]
        frontiers[idx] = frontiers[-1]
        frontiers.pop()

        if random_cell in visited_cells:
            continue

        get_visited_neighbors(visited_neighbors, visited_cells, random_cell,
                              width, height)
        random_neighbor = choice(visited_neighbors)
        remove_wall(grid, random_cell, random_neighbor)
        visited_cells.add(random_cell)
        get_unvisited_neighbors(frontiers, visited_cells, random_cell, width,
                                height)

        if not perfect and random() < imperfection_rate:
            extra_neighbors = [n for n in visited_neighbors
                               if n != random_neighbor]
            for neighbor in extra_neighbors:
                if not would_create_3x3(grid, random_cell, neighbor, width,
                                        height):
                    remove_wall(grid, random_cell, neighbor)
                    break




def display_maze_matrix(grid: list[list[int]]):
    for row in grid:
        for cell in row:
            print(cell, end='')
        print()


def display_maze(grid, width, height):
    for y in range(height):
        # Ligne du haut des cellules
        for x in range(width):
            print("+", end="")
            if grid[y][x] & NORTH:
                print("---", end="")
            else:
                print("   ", end="")
        print("+")

        # Ligne du milieu (avec murs gauche/droite)
        for x in range(width):
            if grid[y][x] & WEST:
                print("|", end="")
            else:
                print(" ", end="")
            print("   ", end="")

        # Mur de droite final
        if grid[y][width - 1] & EAST:
            print("|")
        else:
            print(" ")

    # Dernière ligne (bas du labyrinthe)
    for x in range(width):
        print("+", end="")
        if grid[height - 1][x] & SOUTH:
            print("---", end="")
        else:
            print("   ", end="")
    print("+")


if __name__ == "__main__":
    start = time()
    prim(grid, width, height)
    end = time()
    display_maze(grid, width, height)
    print("\n\n\n\n\n\n\n\n\n\n")
    print("=================================================")
    print(f"    Spell completed in {end - start:.8f} seconds")
    print("=================================================")
    print("\n\n\n\n\n\n\n\n\n\n")
    start = time()
    prim(grid, width, height, False, 0.1)
    end = time()
    display_maze(grid, width, height)
    print("\n\n\n\n\n\n\n\n\n\n")
    print("=================================================")
    print(f"    Spell completed in {end - start:.8f} seconds")
    print("=================================================")
