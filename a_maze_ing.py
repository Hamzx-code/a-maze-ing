# ************************************************************************** #
#                                                                            #
#                                                        :::      ::::::::   #
#   a_maze_ing.py                                      :+:      :+:    :+:   #
#                                                    +:+ +:+         +:+     #
#   By: hhamidi <hhamidi@student.42lyon.fr>        +#+  +:+       +#+        #
#                                                +#+#+#+#+#+   +#+           #
#   Created: 2026/04/23 14:25:36 by hhamidi           #+#    #+#             #
#   Updated: 2026/04/23 14:25:36 by hhamidi          ###   ########.fr       #
#                                                                            #
# ************************************************************************** #

from sys import argv
from pydantic import ValidationError
from parsing import Parsing


def list_to_dict(data: list[str]) -> dict[str, str]:
    config: dict[str, str] = {}
    for element in data:
        if '#' in element:
            element = element.split('#', 1)[0].strip()
        pair = element.split("=", 1)
        if len(pair) == 2:
            config[pair[0].strip()] = pair[1].strip()
    return config


def main(argv: list[str]) -> None:
    if len(argv) == 1:
        print("You must add the config.txt")
        print("python3 a_maze_ing.py config.txt OR make run")
        return
    if argv[1] != "config.txt":
        print("You must use the config.txt")
        return
    try:
        with open("config.txt", 'r') as file:
            file_content: list[str] = file.readlines()
    except FileNotFoundError:
        print(f"config.txt not found, you must create the config file")
    except PermissionError:
        print("We don’t have access to the file (config.txt), "
              "you need to change the file permissions using this command:")
        print("Linux / Mac: chmod +r config.txt")
        print("Windows: icacls config.txt /grant %username%:R")
    except OSError as e:
        print(f"System error: {e}")
    else:
        data: dict[str, str] = list_to_dict(file_content)
        try:
            Parsing(
                width=int(data["WIDTH"]),
                height=int(data["HEIGHT"]),
                entry=tuple(int(x) for x in data["ENTRY"].split(",")),
                exit=tuple(int(x) for x in data["EXIT"].split(",")),
                output_file=data["OUTPUT_FILE"],
                perfect=data.get("PERFECT", "True") == "True",
                animation=data.get("ANIMATION", "True") == "True",
                pathfinding_algo=data.get("PATHFINDING_ALGO", "A*"))
        except ValidationError as e:
            for error in e.errors():
                print(f"Field: {error['loc']}")
                print(f"Error Type: {error['type']}")
                print(f"Error message: {error['msg']}")
                print(f"Input: {error['input']}")
        else:
            print(data)
            print(file_content)



if __name__ == "__main__":
    try:
        main(argv)
    except Exception as e:
        print(e)
