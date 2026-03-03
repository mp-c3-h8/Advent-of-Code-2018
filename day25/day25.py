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


def manhatten(u: Vec4, v: Vec4) -> int:
    return sum(abs(u_i-v_i) for u_i, v_i in zip(u, v))


def num_constellations(points: list[Vec4]) -> int:
    constellations: list[list[Vec4]] = []
    for point in points:
        new_constellations = []
        new_con = [point]
        for con in constellations:
            if any(manhatten(point, v) <= 3 for v in con):
                new_con.extend(con)
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
