# ************************************************************************** #
#                                                                            #
#                                                        :::      ::::::::   #
#   prim_algo.py                                       :+:      :+:    :+:   #
#                                                    +:+ +:+         +:+     #
#   By: hhamidi <hhamidi@student.42lyon.fr>        +#+  +:+       +#+        #
#                                                +#+#+#+#+#+   +#+           #
#   Created: 2026/04/26 23:01:06 by hhamidi           #+#    #+#             #
#   Updated: 2026/04/26 23:01:06 by hhamidi          ###   ########.fr       #
#                                                                            #
# ************************************************************************** #

from random import randint, choice, randrange
from time import time


width = 500
height = 500

NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000

grid = [[0xf] * width for _ in range(height)]


def get_unvisited_neighbors(frontiers: list[tuple[int, int]],
                            visited_cells: set[tuple[int, int]],
                            cell: tuple[int, int],
                            width: int,
                            height: int) -> None:

    (x, y) = cell

    if x > 0 and (x - 1, y) not in visited_cells:
        frontiers.append((x - 1, y))

    if x < width - 1 and (x + 1, y) not in visited_cells:
        frontiers.append((x + 1, y))

    if y > 0 and (x, y - 1) not in visited_cells:
        frontiers.append((x, y - 1))

    if y < height - 1 and (x, y + 1) not in visited_cells:
        frontiers.append((x, y + 1))


def get_visited_neighbors(visited_neighbors: list[tuple[int, int]],
                          visited_cells: set[tuple[int, int]],
                          cell: tuple[int, int],
                          width: int, height: int) -> None:
    (x, y) = cell
    if x > 0 and (x - 1, y) in visited_cells:
        visited_neighbors.append((x - 1, y))

    if x < width - 1 and (x + 1, y) in visited_cells:
        visited_neighbors.append((x + 1, y))

    if y > 0 and (x, y - 1) in visited_cells:
        visited_neighbors.append((x, y - 1))

    if y < height - 1 and (x, y + 1) in visited_cells:
        visited_neighbors.append((x, y + 1))


def remove_wall(grid: list[list[int]], cell: tuple[int, int],
                neighbor: tuple[int, int]):

    cell_x, cell_y = cell
    neighbor_x, neighbor_y = neighbor

    if neighbor_y == cell_y + 1:
        grid[cell_y][cell_x] &= ~SOUTH
        grid[neighbor_y][neighbor_x] &= ~NORTH

    elif neighbor_y == cell_y - 1:
        grid[cell_y][cell_x] &= ~NORTH
        grid[neighbor_y][neighbor_x] &= ~SOUTH

    elif neighbor_x == cell_x + 1:
        grid[cell_y][cell_x] &= ~EAST
        grid[neighbor_y][neighbor_x] &= ~WEST

    elif neighbor_x == cell_x - 1:
        grid[cell_y][cell_x] &= ~WEST
        grid[neighbor_y][neighbor_x] &= ~EAST


def prim_algo(grid: list[list[int]], width: int, height: int):

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
    prim_algo(grid, width, height)
    end = time()
    # display_maze(grid, width, height)
    print("\n\n\n\n\n\n\n\n\n\n")
    print("=================================================")
    print(f"    Spell completed in {end - start:.8f} seconds")
    print("=================================================")
