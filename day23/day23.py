import os.path
import os
import sys
import re
from z3 import Int, If, Abs, Optimize, sat

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


def best_position(nanobots: list[NanoBot]) -> tuple[int, int]:
    solver = Optimize()
    X, Y, Z, R, D = Int("X"), Int("Y"), Int("Z"), Int("R"), Int("D")
    objective = X*0  # dummy to start
    for (x, y, z), r in nanobots:
        objective += If(Abs(X-x)+Abs(Y-y)+Abs(Z-z) <= r, 1, 0)  # type: ignore
    solver.add(R == objective)
    solver.add(D == Abs(X)+Abs(Y)+Abs(Z))  # type: ignore
    solver.maximize(R)  # max number of bots in range
    solver.minimize(D)  # min distance to origin
    assert solver.check() == sat, "Z3 could not solve :("
    model = solver.model()
    return model[R].as_long(), model[D].as_long()  # type: ignore


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    nanobots = create_nanobots(data)
    p1 = strongest_nanobot(nanobots)
    print("Part 1:", p1)

    num_bots, dist = best_position(nanobots)
    print(f"Part 2: {dist} ({num_bots} bots in range)")


if __name__ == "__main__":
    main()
