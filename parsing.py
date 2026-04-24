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
from typing import Any


class MissingKeyError(Exception):
    pass


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

    @model_validator(mode='before')
    @classmethod
    def dict_validator(cls, data: dict[str, Any]) -> dict[str, Any]:
        keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT",
                "ANIMATION", "PATHFINDING_ALGO"]

        for key in keys:
            if key not in data:
                raise MissingKeyError(f"Missing key '{key}' in config file")
            if not data[key] or not data[key].strip():
                raise ValueError(f"Key '{key}' exists but has no value in config file")

        try:
            data["WIDTH"] = int(data["WIDTH"].strip())
            data["HEIGHT"] = int(data["HEIGHT"].strip())
        except ValueError:
            raise ValueError("WIDTH and HEIGHT must be valid integers")

        try:
            entry_position = [nb.strip() for nb in data["ENTRY"].split(',')]
            exit_position = [nb.strip() for nb in data["EXIT"].split(',')]
            if len(entry_position) != 2 or len(exit_position) != 2:
                raise ValueError("ENTRY and EXIT must follow the 'x,y' format")
            data["ENTRY"] = tuple(int(nb) for nb in entry_position)
            data["EXIT"] = tuple(int(nb) for nb in exit_position)
        except ValueError as e:
            raise ValueError(f"Invalid ENTRY or EXIT format: {e}")

        perfect_value = data["PERFECT"].strip().lower()
        if perfect_value not in ("true", "false"):
            raise ValueError("PERFECT value must be 'True' or 'False'")

        animation_value = data["ANIMATION"].strip().lower()
        if animation_value not in ("true", "false"):
            raise ValueError("ANIMATION value must be 'True' or 'False'")

        return {"width": data["WIDTH"], "height": data["HEIGHT"],
                "entry": data["ENTRY"], "exit": data["EXIT"],
                "output_file": data["OUTPUT_FILE"].strip(),
                "perfect": perfect_value == "true",
                "animation": animation_value == "true",
                "pathfinding_algo": data["PATHFINDING_ALGO"].strip()}

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



