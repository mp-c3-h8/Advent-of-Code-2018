import numpy as np
from scipy.ndimage import convolve
from utils import timed


def power_grid(grid_serial_number: int) -> np.ndarray:
    indices = np.indices((300, 300), dtype=int)
    indices += 1  # 0-indexing to 1-indexing
    grid = indices[1] + 10
    grid = (grid * indices[0] + grid_serial_number) * grid
    grid = grid % 1_000 // 100 - 5
    return grid


def largest_total_power(grid_serial_number: int) -> str:
    KERNEL = np.ones((3, 3), dtype=int)
    grid = power_grid(grid_serial_number)
    cells = convolve(grid, KERNEL, mode="constant")
    coords = np.unravel_index(np.argmax(cells), cells.shape)
    res = f"{coords[1]},{coords[0]}"  # no offsetting needed (top-left instead of center)

    return res


def summed_area(grid: np.ndarray) -> np.ndarray:
    summed = np.zeros((301, 301), dtype=int)  # left pad with zero
    for y in range(1, 301):
        for x in range(1, 301):
            summed[y, x] = grid[y-1, x-1] + summed[y-1, x] + summed[y, x-1] - summed[y-1, x-1]

    return summed


@timed("Part 2 partial sums")
# https://en.wikipedia.org/wiki/Summed-area_table
def part2_partial_sums(grid_serial_number: int) -> str:
    grid = power_grid(grid_serial_number)  # (300,300)
    summed = summed_area(grid)  # (301,301)
    best = -1
    best_width = -1
    coords = (-1, -1)

    for w in range(1, 301):
        # summing squares with width w
        # top left + bottom right - top right - bottom left
        cells = summed[:-w, :-w] + summed[w:, w:] - summed[:-w, w:] - summed[w:, :-w]
        m = np.max(cells)
        if m > best:
            best = m
            best_width = w
            coords = np.unravel_index(np.argmax(cells), cells.shape)

    return f"{coords[1]+1},{coords[0]+1},{best_width}"


def main() -> None:
    GRID_SERIAL_NUMBER = 9798
    p1 = largest_total_power(GRID_SERIAL_NUMBER)
    print("Part 1:", p1)
    p2 = part2_partial_sums(GRID_SERIAL_NUMBER)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
