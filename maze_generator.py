# ************************************************************************** #
#                                                                            #
#                                                        :::      ::::::::   #
#   maze_generator.py                                  :+:      :+:    :+:   #
#                                                    +:+ +:+         +:+     #
#   By: hhamidi <hhamidi@student.42lyon.fr>        +#+  +:+       +#+        #
#                                                +#+#+#+#+#+   +#+           #
#   Created: 2026/04/25 19:16:13 by hhamidi           #+#    #+#             #
#   Updated: 2026/04/25 19:16:13 by hhamidi          ###   ########.fr       #
#                                                                            #
# ************************************************************************** #



class MazeGenerator:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = [[0xf] * self.width for _ in range(self.height)]


    def display_grid(self):
        for row in self.grid:
            for cell in row:
                print(cell, end="")
            print()




if __name__ == "__main__":
    maze = MazeGenerator(20, 20)
    maze.display_grid()
