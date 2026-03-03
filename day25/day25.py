import os.path
import os
import sys
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

type Vec4 = tuple[int, int, int, int]


def parse(data: str) -> list[Vec4]:
    res = []
    regexp = re.compile(r"-?\d+")
    for line in data.splitlines():
        x, y, z, t = map(int, regexp.findall(line))
        res.append((x, y, z, t))
    return res


def num_constellations(points: list[Vec4]) -> int:
    constellations: list[set[Vec4]] = []
    for (x, y, z, t) in points:
        new_constellations = []
        new_con = {(x, y, z, t)}
        for con in constellations:
            if any(abs(x-x2) + abs(y-y2) + abs(z-z2) + abs(t-t2) <= 3 for x2, y2, z2, t2 in con):
                new_con.update(con)
            else:
                new_constellations.append(con)

        new_constellations.append(new_con)
        constellations = new_constellations
    return len(constellations)


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    points = parse(data)
    p1 = num_constellations(points)
    print("Part 1:", p1)


if __name__ == "__main__":
    main()
