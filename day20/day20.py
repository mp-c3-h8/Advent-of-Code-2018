import os.path
import os
from utils import timed
from collections import defaultdict, deque

type Pos = tuple[int, int]  # (y,x) y downwards
type Graph = defaultdict[Pos, set[Pos]]
type Item = tuple[int, Pos]


def create_graph(data: str, origin: Pos) -> Graph:
    DIRS = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}
    graph: Graph = defaultdict(set)
    positions: set[Pos] = {origin}
    starts: set[Pos] = {origin}
    ends: set[Pos] = set()
    stack: list[tuple[set[Pos], set[Pos]]] = []  # list of (starts,ends)

    for c in data[1:-1]:
        if c == "(":
            stack.append((starts, ends))  # push current state for later use
            starts = positions  # current positions are the starts for new group
            ends = set()
        elif c == "|":
            ends.update(positions)
            positions = starts  # reset to starting points
        elif c == ")":
            positions.update(ends)  # close group
            starts, ends = stack.pop()  # pop previous state
        else:  # letter
            d = DIRS[c]
            new_positions = set()
            for pos in positions:
                new_pos = (pos[0]+d[0], pos[1]+d[1])
                graph[pos].add(new_pos)
                new_positions.add(new_pos)
            positions = new_positions
    return graph


def dijkstra(graph: Graph, start: Pos) -> tuple[int, int]:
    init: Item = (0, start)  # (steps,pos)
    q: deque[Item] = deque([init])  # dont need priority q here
    shortest_paths: dict[Pos, int] = {start: 0}
    done: set[Pos] = set()

    while q:
        steps, pos = q.popleft()

        if pos in done:
            continue
        done.add(pos)

        for new_pos in graph[pos]:
            if new_pos in done:
                continue
            new_steps = steps + 1
            if new_pos in shortest_paths and shortest_paths[new_pos] <= new_steps:
                continue
            shortest_paths[new_pos] = new_steps
            q.append((new_steps, new_pos))

    p1 = max(shortest_paths.values())
    p2 = sum(steps >= 1000 for steps in shortest_paths.values())
    return p1, p2


@timed("All")
def main() -> None:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    ORIGIN: Pos = (0, 0)
    graph = create_graph(data, ORIGIN)
    p1, p2 = dijkstra(graph, ORIGIN)

    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
