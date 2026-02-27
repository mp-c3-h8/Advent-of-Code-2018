import os.path
import os
from utils import timed
import re

type Pos = tuple[int, int]  # (y,x) y downwards
type Grid = dict[Pos, str]


def create_grid(data: str) -> Grid:
    grid = {}
    regexp = re.compile(r"-?\d+")
    for line in data.splitlines():
        c1, c2_from, c2_to = map(int, regexp.findall(line))
        c1_is_x = line[0] == "x"
        for c2 in range(c2_from, c2_to+1):
            pos = (c2, c1) if c1_is_x else (c1, c2)
            grid[pos] = "█"
    return grid


def print_grid(grid: Grid, flowing: set[Pos]) -> None:
    y_max, x_max = map(max, *grid)
    y_min, x_min = map(min, *grid)

    for y in range(y_min, y_max+1):
        for x in range(x_min, x_max+1):
            print("|" if (y, x) in flowing else grid[(y, x)] if (y, x) in grid else " ", end="")
        print()


def drop_water(grid: Grid, pos: Pos, y_max: int) -> Pos | None:
    y, x = pos
    while y <= y_max:
        if (y, x) in grid:
            return (y-1, x)
        y += 1
    return None


def extend_left_and_right(grid: Grid, pos: Pos) -> tuple[list[Pos], list[Pos]]:
    new_outlets: list[Pos] = []
    walls_hit: list[Pos] = []
    for x_direction in (-1, 1):
        y, x = pos
        while True:
            if (y+1, x) not in grid:
                new_outlets.append((y, x))
                break
            if (y, x+x_direction) in grid:
                walls_hit.append((y, x))
                break
            x += x_direction
    return walls_hit, new_outlets


def water_reach(grid: Grid) -> tuple[int, int]:
    num_clay = len(grid)
    y_max, x_max = map(max, *grid)
    y_min, x_min = map(min, *grid)
    outlets_done: set[Pos] = set()
    outlets: list[Pos] = [(y_min, 500)]

    # add all settled water
    while outlets:
        curr_outlet = outlets[-1]

        # outlet already done?
        if curr_outlet in outlets_done:
            outlets.pop()
            continue

        # drop a droplet till it hits clay or settled water
        pos = drop_water(grid, curr_outlet, y_max)

        # out of y-bounds
        if pos is None:
            outlets_done.add(outlets.pop())
            continue

        while True:
            # check to the left and right
            # len(walls_hit) + len(new_outlets) == 2
            walls_hit, new_outlets = extend_left_and_right(grid, pos)

            if len(new_outlets) != 0:
                outlets_done.add(outlets.pop())
                outlets.extend(new_outlets)
                break

            # water enclosed between two walls
            y, x_from = walls_hit[0]  # left
            y, x_to = walls_hit[1]  # right
            for x in range(x_from, x_to+1):
                grid[(y, x)] = "~"

            # can raise higher than the outlet itself (to fill ie a bathtub)
            pos = (pos[0]-1, pos[1])

    # add remaining reachable squares
    flowing: set[Pos] = set()
    outlets_done = set()
    outlets = [(y_min, 500)]
    while outlets:
        curr_outlet = outlets.pop()
        if curr_outlet in outlets_done:
            continue
        outlets_done.add(curr_outlet)

        pos = drop_water(grid, curr_outlet, y_max)
        if pos is None:  # out of y-bounds
            y_to = y_max + 1
        else:
            y_to = pos[0] + 1
            walls_hit, new_outlets = extend_left_and_right(grid, pos)
            left, right = sorted(walls_hit+new_outlets)
            for x in range(left[1], right[1]+1):
                flowing.add((pos[0], x))
            outlets.extend(new_outlets)

        for y in range(curr_outlet[0], y_to):
            flowing.add((y, curr_outlet[1]))

    num_at_rest = len(grid) - num_clay
    num_flowing = len(flowing)
    # print_grid(grid, flowing)

    return num_at_rest, num_flowing


@timed("All")
def main() -> None:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    grid = create_grid(data)
    num_at_rest, num_flowing = water_reach(grid)
    print("Part 1:", num_at_rest + num_flowing)
    print("Part 2:", num_at_rest)


if __name__ == "__main__":
    main()
