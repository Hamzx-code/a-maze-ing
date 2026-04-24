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
from parsing import Parsing, MissingKeyError, PositionError
from parsing import FileNameError,AlgoNameError


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
        print("You must add the config file")
        print("python3 a_maze_ing.py <file_name.txt> OR make run")
        return
    if not argv[1].endswith(".txt"):
        print("You must use a text file (exemple: config.txt)")
        return
    try:
        with open(argv[1], 'r') as file:
            file_content: list[str] = file.readlines()
    except FileNotFoundError:
        print(f"{argv[1]} not found, you must create the config file")
    except PermissionError:
        print(f"We don’t have access to the file ({argv[1]}), "
              "you need to change the file permissions using this command:")
        print("Linux / Mac: chmod +r <file_name.txt>")
        print("Windows: icacls <file_name.txt> /grant %username%:R")
    except OSError as e:
        print(f"System error: {e}")
    else:
        data: dict[str, str] = list_to_dict(file_content)
        try:
            config = Parsing.model_validate(data)
        except MissingKeyError as e:
            print(f"Config error: {e}")
        except PositionError as e:
            print(f"Position error: {e}")
        except FileNameError as e:
            print(f"File name error: {e}")
        except AlgoNameError as e:
            print(f"Algorithm error: {e}")
        except ValidationError as e:
            for error in e.errors():
                print(f"[{error['loc']}] {error['msg']} (got: {error['input']})")
        else:
            print(file_content)
            print(data)
            print(config)


if __name__ == "__main__":
    try:
        main(argv)
    except Exception as e:
        print(e)
