import os.path
import os
from utils import timed
import numpy as np
from scipy.ndimage import convolve


def conway_step(grid: np.ndarray) -> np.ndarray:
    KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.int8)
    new_grid = grid.copy()
    conv = convolve(grid, KERNEL, mode="constant")
    lumberyards, trees = np.divmod(conv, 9)
    new_grid[(grid == 0) & (trees >= 3)] = 1
    new_grid[(grid == 1) & (lumberyards >= 3)] = 9
    new_grid[(grid == 9) & ((trees == 0) | (lumberyards == 0))] = 0
    return new_grid


def resource_value(grid: np.ndarray) -> int:
    return (grid == 1).sum() * (grid == 9).sum()


def conway(grid: np.ndarray, steps: int) -> int:
    for _ in range(steps):
        grid = conway_step(grid)
    return resource_value(grid)


def conway_with_period(grid: np.ndarray, steps: int) -> int:
    # find period
    seen: dict[tuple[int, ...], int] = {tuple(grid.flatten()): 0}
    for i in range(1, 10**6):
        grid = conway_step(grid)
        state = tuple(grid.flatten())
        if state in seen:
            break
        seen[state] = i
    else:
        raise ValueError("Max iterations reached.")

    # calc remaining steps
    before_period = seen[state]
    period = i - before_period
    remaining = (steps-before_period) % period

    return conway(grid, remaining)


@timed("All")
def main() -> None:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    array = [[9 if c == "#" else 1 if c == "|" else 0 for c in row] for row in data.splitlines()]
    grid = np.array(array, dtype=np.int8)
    STEPS = 1_000_000_000

    print("Part 1:", conway(grid.copy(), 10))
    print("Part 2:", conway_with_period(grid, STEPS))


if __name__ == "__main__":
    main()
