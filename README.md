*This project has been created as part of the 42 curriculum by hhamidi, ramaroud.*

# A-Maze-ing

A maze generator written in Python that creates perfect or imperfect mazes, displays them visually, and exports them in a hexadecimal format.

---

## Description

A-Maze-ing generates mazes from a configuration file. It uses **Prim's algorithm** to build the maze structure, supports both perfect mazes (single path between entry and exit) and imperfect ones (multiple paths), and finds the shortest path using **A\***. The maze is exported to a file using a hexadecimal wall encoding, and displayed visually in the terminal or via a graphical window.

The maze always contains a visible **"42" pattern** formed by fully closed cells, and corridors are never wider than 2 cells.

---

## Instructions

### Requirements

- Python 3.10 or later
- pip

### Installation

```bash
make install
```

### Run

```bash
make run
# or
python3 a_maze_ing.py config.txt
```

### Debug

```bash
make debug
```

### Lint

```bash
make lint
# or
make lint-strict 
```

### Clean

```bash
make clean
```

---

## Configuration file

The configuration file uses one `KEY=VALUE` pair per line. Lines starting with `#` are treated as comments and ignored.

### Format

```txt
# Maze configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

### Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `WIDTH` | int (3–250) | ✅ | Number of columns |
| `HEIGHT` | int (3–250) | ✅ | Number of rows |
| `ENTRY` | x,y | ✅ | Entry coordinates |
| `EXIT` | x,y | ✅ | Exit coordinates |
| `OUTPUT_FILE` | .txt filename | ✅ | Output file name |
| `PERFECT` | True/False | ✅ | Perfect maze (single path) |
| `SEED` | string | ✅ | Random seed for reproducibility |

---

## Output file format

Each cell is encoded as a single hexadecimal digit representing which walls are closed:

| Bit | Direction |
|---|---|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

A closed wall sets the bit to `1`, open means `0`.

Example: `F` (binary `1111`) = all walls closed. `A` (binary `1010`) = East and West walls closed.

Cells are stored row by row, one row per line. After an empty line, three additional lines contain:
1. Entry coordinates
2. Exit coordinates
3. Shortest path from entry to exit using `N`, `E`, `S`, `W`

---

## Maze generation algorithm — Prim's algorithm

The maze is generated using a **randomized version of Prim's algorithm**, originally designed to find minimum spanning trees in graphs.

### How it works

1. Pick a random starting cell and mark it as visited.
2. Add its unvisited neighbors to a frontier list.
3. While the frontier is not empty:
   - Pick a random cell from the frontier.
   - If it is already visited, skip it.
   - Find one of its visited neighbors randomly.
   - Remove the wall between them.
   - Mark the cell as visited.
   - Add its unvisited neighbors to the frontier.

### Why Prim?

- Generates visually **organic mazes** with many short branches.
- Naturally produces **perfect mazes** (no cycles, full connectivity).
- Easy to animate step by step.
- Well suited for imperfect maze generation by opening extra walls during generation.

### Imperfect mazes

When `PERFECT=False`, at each step of Prim, there is a chance (controlled by `IMPERFECTION_RATE`) to open an extra wall toward another visited neighbor. This creates cycles while respecting the **no 3×3 open area** constraint — checked before each extra wall is opened using the `would_create_3x3` function.

---

## Pathfinding — A\*

The shortest path between entry and exit is found using **A\*** with the **Manhattan distance** as heuristic:

```
h(n) = |n.x - exit.x| + |n.y - exit.y|
```

A\* explores cells in order of `f(n) = g(n) + h(n)` where `g(n)` is the real cost from the start. This guarantees the shortest path is found efficiently.

---

## Reusable module — `mazegen`

The maze generation logic is encapsulated in the `MazeGenerator` class, available as a standalone pip-installable package named `mazegen-*`.

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic usage

```python
from mazegen.PrimGenerator import PrimGenerator
from mazegen.Vec2 import Vec2

# Create a 20x15 perfect maze with a fixed seed
maze = PrimGenerator(
    width=20,
    height=15,
    start_pos=Vec2(0, 0),
    end_pos=Vec2(19, 14),
    seed="42",
    is_perfect=True
)

maze.generate()
```

### Custom parameters

```python
from mazegen.PrimGenerator import PrimGenerator
from mazegen.Vec2 import Vec2

# Imperfect maze
maze = PrimGenerator(
    width=30,
    height=30,
    start_pos=Vec2(0, 0),
    end_pos=Vec2(19, 14),
    seed="42",
    is_perfect=False,
)
maze.generate()
```

### Building the package

```bash
pip install build
python3 -m build
# outputs: dist/mazegen-1.0.0-py3-none-any.whl
```

The package source files are located at the root of the repository.

---

## Bonus Features

- **Deterministic generation using a seed**  
  The maze generation is fully reproducible using a custom seed value, allowing identical mazes to be regenerated for debugging and testing purposes.

- **Dynamic “42 pattern” color adaptation**  
  The “42” pattern embedded in the maze dynamically adapts to the selected maze color, ensuring visual consistency regardless of the rendering theme.

---

## Team and project management

### Roles

| Member | Role |
|---|---|
| hhamidi | Maze generation, pathfinding, parsing |
| ramaroud | Parsing, maze, visual rendering |

### Planning

Initial plan:
1. **Configuration parsing and validation**
   Implemented first to ensure a reliable and robust base for all subsequent components.

2. **Maze core structure (Maze class)**
   Designed the main Maze class to encapsulate generation logic, grid representation, and constraints.

3. **Maze generation (Prim’s algorithm)**
   Implemented randomized Prim’s algorithm as the core maze generation method.

4. **Pathfinding (A\*)**
   Added shortest path computation using A* with Manhattan distance heuristic.

5. **Output system**
   Implemented hexadecimal encoding format for maze export.

6. **Visual rendering (MLX)**
   Integrated MiniLibX for graphical visualization of the maze and solution path.

7. **Reusable package (mazegen)**
   Refactored core generation logic into a standalone Python package installable via pip

During development, some parts took longer than expected:
- The Maze class design required refactoring to keep generation and rendering decoupled.
- The 3×3 constraint implementation (`would_create_3x3`) was more complex than anticipated.
- The MLX-based visualization required additional time for integration and debugging.

### What worked well

- Using Pydantic for config validation made error handling clean and readable.
- Separating concerns into small focused functions made debugging much easier.

### What could be improved

- Supporting multiple algorithms (Kruskal, DFS) as a bonus.

### Tools used

- Python 3.13
- Pydantic v2 — config validation
- mypy — static type checking
- flake8 — code style

---


## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Prim's algorithm — Wikipedia](https://en.wikipedia.org/wiki/Prim%27s_algorithm)
- [A* search algorithm — Wikipedia](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [Pydantic v2 documentation](https://mintlify.wiki/pydantic/pydantic)
- [Python heapq documentation](https://www.geeksforgeeks.org/python/heap-queue-or-heapq-in-python/)

### AI usage

Claude was used for:
- Explaining algorithmic concepts (Prim, A*).
- Drafting this README structure.
