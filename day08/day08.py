import os.path
import os
from timeit import default_timer as timer
from collections import deque, Counter


class Node:
    __slots__ = ["childs", "meta"]

    def __init__(self, numbers: deque[int]) -> None:
        num_childs = numbers.popleft()
        num_meta = numbers.popleft()

        self.childs: list[Node] = []
        for _ in range(num_childs):
            child = Node(numbers)
            self.childs.append(child)

        self.meta: list[int] = []
        for _ in range(num_meta):
            self.meta.append(numbers.popleft())

    def sum_meta(self) -> int:
        return sum(self.meta) + sum(child.sum_meta() for child in self.childs)

    def value(self) -> int:
        if len(self.childs) == 0:
            return sum(self.meta)
        else:
            counter = Counter(self.meta)
            return sum(count * self.childs[meta-1].value() for meta, count in counter.items() if 0 < meta <= len(self.childs))


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

numbers = deque([int(c) for c in data.split(" ")])

tree = Node(numbers)
print("Part 1:", tree.sum_meta())
print("Part 2:", tree.value())


e = timer()
print(f"time: {e-s}")
