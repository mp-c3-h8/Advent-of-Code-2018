import os.path
import os
from collections import Counter
from itertools import combinations


def checksum(data: str) -> int:
    double = 0
    triple = 0
    for box_id in data.splitlines():
        counter = Counter(box_id)
        double += 2 in counter.values()
        triple += 3 in counter.values()
    return double*triple


def prototype_fabric(data: str) -> str:
    for idx, other_idx in combinations(data.splitlines(), 2):
        differ = None
        for i, (c, oc) in enumerate(zip(idx, other_idx)):
            if c != oc:
                if differ is not None:  # more than one different character
                    differ = None
                    break
                differ = i
        if differ is not None:
            return idx[:differ] + idx[differ+1:]
    raise ValueError("Prototype fabric not found :(")


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()


print("Part 1:", checksum(data))
print("Part 2:", prototype_fabric(data))
