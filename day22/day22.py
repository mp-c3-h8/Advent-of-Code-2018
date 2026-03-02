import os.path
import os
import sys
import re
from typing import Iterator
from heapq import heapify, heappop, heappush

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

type Pos = tuple[int, int]  # (y,x) y downwards
type Region = int
type Tool = int
type Grid = list[list[int]]
type State = tuple[Pos, Tool]


def parse(data: str) -> tuple[int, Pos]:
    d, x, y = re.findall(r"\d+", data)
    return int(d), (int(y), int(x))


def risk_level(depth: int, target: Pos) -> tuple[int, Grid]:
    EXTRA = 200
    dimy = target[0] + 1
    dimx = target[1] + 1
    erosion: Grid = [[0]*(dimx+EXTRA) for _ in range((dimy+EXTRA))]
    region_type: Grid = [[0]*(dimx+EXTRA) for _ in range((dimy+EXTRA))]

    # y == 0
    erosion[0] = [(16807*x + depth) % 20183 for x in range((dimx+EXTRA))]
    region_type[0] = [(16807*x + depth) % 20183 % 3 for x in range((dimx+EXTRA))]

    # x == 0
    for y in range(len(erosion)):
        erosion[y][0] = (y * 48271 + depth) % 20183
        region_type[y][0] = erosion[y][0] % 3

    # y > 0 and x > 0
    for y in range(1, (dimy+EXTRA)):
        for x in range(1, (dimx+EXTRA)):
            erosion[y][x] = (erosion[y-1][x] * erosion[y][x-1] + depth) % 20183
            region_type[y][x] = erosion[y][x] % 3

    # target
    erosion[target[0]][target[1]] = (0 + depth) % 20183
    region_type[target[0]][target[1]] = erosion[target[0]][target[1]] % 3

    risk = sum(sum(row[:dimx]) for row in region_type[:dimy])
    return risk, region_type


# TOOLS:
# 0 = neither
# 1 = torch
# 2 = climbing gear
def tools_for_region(region: Region) -> Iterator[Tool]:
    # below simplified
    yield from (tool for tool in (0, 1, 2) if tool != region)

    # if region == 0:  # rocky
    #     yield from (1, 2)
    # elif region == 1:  # wet
    #     yield from (0, 2)
    # elif region == 2:  # narrow
    #     yield from (0, 1)
    # else:
    #     raise ValueError(f"Region type {region} invalid.")


def tool_valid_for_region(tool: Tool, region: Region) -> bool:
    # below simplified
    return tool != region

    if tool == 0:  # neither
        return region != 0  # not rocky
    elif tool == 1:  # torch
        return region != 1  # not wet
    elif tool == 2:  # climbing gear
        return region != 2  # not wet
    raise ValueError(f"Tool {tool} invalid.")


def rescue_friend(grid: Grid, target: Pos) -> int:
    DIRS: list[Pos] = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    start: Pos = (0, 0)
    starting_tool: Tool = 1  # torch
    target_tool: Tool = 1  # torch
    start_state: State = (start, starting_tool)
    target_state: State = (target, target_tool)
    q: list[tuple[int, int, State]] = [(0, 0, start_state)]  # (prio,minutes,state)
    heapify(q)
    shortest_paths: dict[State, int] = {start_state: 0}  # state: minutes
    done: set[State] = set()

    i = k = 0
    while q:
        prio, minutes, state = heappop(q)
        pos, tool = state

        i += 1
        if state in done:
            continue
        done.add(state)

        k += 1
        if pos == target:
            print(f"i={i},k={k}")
            return minutes + (tool != target_tool) * 7

        region = grid[pos[0]][pos[1]]
        for new_tool in tools_for_region(region):
            minutes_plus_toolchange = minutes + (tool != new_tool) * 7
            for d in DIRS:
                new_pos = (pos[0]+d[0], pos[1]+d[1])
                if new_pos[0] < 0 or new_pos[1] < 0:
                    continue

                new_region = grid[new_pos[0]][new_pos[1]]
                if not tool_valid_for_region(new_tool, new_region):
                    continue

                new_state = (new_pos, new_tool)
                if new_state in done:
                    continue

                new_minutes = minutes_plus_toolchange + 1
                if new_state in shortest_paths and shortest_paths[new_state] <= new_minutes:
                    continue

                heuristic = abs(target[0]-new_pos[0]) + abs(target[1]-new_pos[1]) + (new_tool != target_tool)*7
                new_prio = new_minutes + heuristic
                heappush(q, (new_prio, new_minutes, new_state))
    raise ValueError("No rescue path found :(")


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    depth, target = parse(data)
    risk, grid = risk_level(depth, target)
    print("Part 1:", risk)

    p2 = rescue_friend(grid, target)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
