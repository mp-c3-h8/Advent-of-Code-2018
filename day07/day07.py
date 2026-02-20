import os.path
import os
from collections import defaultdict, Counter
from heapq import heapify, heappop, heappush

type Node = str  # uppercase letter
type Graph = defaultdict[Node, list[Node]]
type Time = int


def create_graph(data: str) -> Graph:
    graph = defaultdict(list)
    for line in data.splitlines():
        split = line.split(" ")
        node = split[1]
        other_node = split[-3]
        graph[node].append(other_node)
    return graph


def topological_sort(graph: Graph) -> list[Node]:
    # using Kahn's ALgorithm
    tsort: list[Node] = []
    indegree: Counter = Counter({node: 0 for node in graph})
    for other_nodes in graph.values():
        indegree.update(other_nodes)

    q: list[Node] = [node for node, count in indegree.items() if count == 0]
    assert len(q) > 0
    heapify(q)

    while q:
        node = heappop(q)
        tsort.append(node)

        # "remove" node
        for other_node in graph[node]:
            indegree[other_node] -= 1
            if indegree[other_node] == 0:
                heappush(q, other_node)

    return tsort


def construction_duration(graph: Graph) -> int:
    indegree: Counter = Counter({node: 0 for node in graph})
    for other_nodes in graph.values():
        indegree.update(other_nodes)

    Q_steps: list[Node] = [node for node, count in indegree.items() if count == 0]
    heapify(Q_steps)
    assert len(Q_steps) > 0

    Q_workers: list[tuple[Time, Node]] = []  # (ending_time,step)
    heapify(Q_workers)

    curr_time: Time = 0
    construction: list[tuple[Time, Node]] = []

    while Q_steps or Q_workers:
        # distribute work to workers
        n = min(5-len(Q_workers), len(Q_steps))
        for _ in range(n):
            step = heappop(Q_steps)
            # ascii: A = 65, ... , Z = 90
            ending_time = curr_time + ord(step) - 4
            heappush(Q_workers, (ending_time, step))

        # either all workers are occupied
        # or prerequisite step has to finish
        # => fast forward time (finish earliest job)
        curr_time, step_done = heappop(Q_workers)
        construction.append((curr_time, step_done))

        # are new steps available?
        for next_step in graph[step_done]:
            indegree[next_step] -= 1
            if indegree[next_step] == 0:
                heappush(Q_steps, next_step)

    return construction[-1][0]


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

graph = create_graph(data)
tsort = topological_sort(graph)
print("Part 1:", "".join(tsort))
print("Part 2:", construction_duration(graph))
