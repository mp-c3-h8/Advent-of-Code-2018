import os.path
import os
import sys
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


type Pos = tuple[int, int, int]  # (x,y,z)
type NanoBot = tuple[Pos, int]  # (pos,signal_radius)


def create_nanobots(data: str) -> list[NanoBot]:
    nanobots = []
    regexp = re.compile(r"-?\d+")
    for line in data.splitlines():
        x, y, z, r = map(int, regexp.findall(line))
        nanobots.append(((x, y, z), r))
    return nanobots


def strongest_nanobot(nanobots: list[NanoBot]) -> int:
    strongest = max(nanobots, key=lambda n: n[1])
    (sx, sy, sz), sr = strongest
    res = 0
    for nanobot in nanobots:
        diff = abs(sx-nanobot[0][0]) + abs(sy-nanobot[0][1]) + abs(sz-nanobot[0][2])
        if diff <= sr:
            res += 1
    return res


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    nanobots = create_nanobots(data)
    p1 = strongest_nanobot(nanobots)
    print("Part 1:", p1)


if __name__ == "__main__":
    main()
