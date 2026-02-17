import os.path
import os

type Polymer = list[str]


def collapse_polymer(polymer: Polymer, remove: str | None = None) -> Polymer:
    collapsed: list[str] = []
    for unit in polymer:
        if remove is not None and (remove == unit or remove.upper() == unit):
            continue
        if len(collapsed) > 0 and abs(ord(collapsed[-1])-ord(unit)) == 32:
            collapsed.pop()
        else:
            collapsed.append(unit)
    return collapsed


def shortest_removal(polymer: Polymer) -> int:
    removal_pool = set(unit for unit in polymer if unit.islower())
    return min(len(collapse_polymer(polymer, letter)) for letter in removal_pool)


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

collapsed = collapse_polymer(list(data))
print("Part 1:", len(collapsed))


print("Part 2:", shortest_removal(collapsed))
