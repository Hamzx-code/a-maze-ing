# ************************************************************************** #
#                                                                            #
#                                                        :::      ::::::::   #
#   parsing.py                                         :+:      :+:    :+:   #
#                                                    +:+ +:+         +:+     #
#   By: hhamidi <hhamidi@student.42lyon.fr>        +#+  +:+       +#+        #
#                                                +#+#+#+#+#+   +#+           #
#   Created: 2026/04/23 13:33:59 by hhamidi           #+#    #+#             #
#   Updated: 2026/04/23 13:33:59 by hhamidi          ###   ########.fr       #
#                                                                            #
# ************************************************************************** #

from pydantic import BaseModel, Field, model_validator


class PositionError(Exception):
    pass


class FileNameError(Exception):
    pass


class AlgoNameError(Exception):
    pass


class Parsing(BaseModel):
    width: int = Field(ge=3, le=1000)
    height: int = Field(ge=3, le=1000)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str = Field(min_length=5, max_length=50)
    perfect: bool = True
    animation: bool = True
    pathfinding_algo: str = Field(default="A*",min_length=2, max_length=10)

    @model_validator(mode='after')
    def config_validator(self) -> 'Parsing':
        allowed_algos = {"A*", "BFS"}
        if self.entry[0] < 0 or self.entry[1] < 0 :
            raise PositionError("Entry position coordinates must be non-negative")
        if self.entry[0] >= self.width or self.entry[1] >= self.height:
            raise PositionError(f"Entry position {self.entry} is out of "
                                f"grid bounds ({self.width}x{self.height})")
        if self.exit[0] < 0 or self.exit[1] < 0:
            raise PositionError("Exit position coordinates must be non-negative")
        if self.exit[0] >= self.width or self.exit[1] >= self.height:
            raise PositionError(f"Exit position {self.exit} is out of "
                                f"grid bounds ({self.width}x{self.height})")
        if self.entry == self.exit:
            raise PositionError("Entry and exit positions must be different")
        if not self.output_file.endswith(".txt"):
            raise FileNameError("Output file must have a '.txt' extension.")
        if self.pathfinding_algo not in allowed_algos:
            raise AlgoNameError(f"Unknown algorithm '{self.pathfinding_algo}'."
                                " Allowed values are: "
                                f"{', '.join(allowed_algos)}")
        return self



