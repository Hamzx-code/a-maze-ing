# ************************************************************************** #
#                                                                            #
#                                                        :::      ::::::::   #
#   prim_utils.py                                      :+:      :+:    :+:   #
#                                                    +:+ +:+         +:+     #
#   By: hhamidi <hhamidi@student.42lyon.fr>        +#+  +:+       +#+        #
#                                                +#+#+#+#+#+   +#+           #
#   Created: 2026/04/29 13:29:01 by hhamidi           #+#    #+#             #
#   Updated: 2026/04/29 13:29:01 by hhamidi          ###   ########.fr       #
#                                                                            #
# ************************************************************************** #



NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000

def get_unvisited_neighbors(frontiers: list[tuple[int, int]],
                            visited_cells: set[tuple[int, int]],
                            cell: tuple[int, int],
                            width: int,
                            height: int) -> None:

    x, y = cell

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
    x, y = cell
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

    cx, cy = cell
    nx, ny = neighbor

    if ny == cy + 1:
        grid[cy][cx] &= ~SOUTH
        grid[ny][nx] &= ~NORTH

    elif ny == cy - 1:
        grid[cy][cx] &= ~NORTH
        grid[ny][nx] &= ~SOUTH

    elif nx == cx + 1:
        grid[cy][cx] &= ~EAST
        grid[ny][nx] &= ~WEST

    elif nx == cx - 1:
        grid[cy][cx] &= ~WEST
        grid[ny][nx] &= ~EAST


def would_create_3x3(grid: list[list[int]],cell: tuple[int, int],
                     neighbor: tuple[int, int],
                     width: int, height: int) -> bool:
    cx, cy = cell
    nx, ny = neighbor

    if ny == cy + 1:
        wall_a, wall_b = SOUTH, NORTH
    elif ny == cy - 1:
        wall_a, wall_b = NORTH, SOUTH
    elif nx == cx + 1:
        wall_a, wall_b = EAST, WEST
    elif nx == cx - 1:
        wall_a, wall_b = WEST, EAST
    else:
        return False

    for start_y in range(cy - 2, cy + 1):
        for start_x in range(cx - 2, cx + 1):

            if (start_y < 0 or start_x < 0
                or start_y + 2 >= height or start_x + 2 >= width):
                continue

            zone_open = True

            for dy in range(3):
                for dx in range(3):
                    zy = start_y + dy
                    zx = start_x + dx
                    cell_val = grid[zy][zx]

                    if (zx, zy) == (cx, cy):
                        cell_val &= ~wall_a
                    if (zx, zy) == (nx, ny):
                        cell_val &= ~wall_b

                    if dx < 2 and (cell_val & EAST):
                        zone_open = False
                        break
                    if dy < 2 and (cell_val & SOUTH):
                        zone_open = False
                        break

                if not zone_open:
                    break
            if zone_open:
                return True
    return False

