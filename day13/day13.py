import os.path
import os
from typing import Iterator
from itertools import cycle
from utils import timed

type Pos = complex  # y=1j downwards
type Dir = complex
type Grid = dict[Pos, str]


class Cart:
    __slots__ = ["pos", "dir", "turns"]

    def __init__(self, pos: Pos, dir: Dir) -> None:
        self.pos = pos
        self.dir = dir
        self.turns: Iterator[Dir] = cycle([-1j, 1, 1j])

    def turn(self) -> None:
        self.dir *= next(self.turns)

    def move(self) -> None:
        self.pos += self.dir

    def take_curve(self, curve: str) -> None:
        CURVE: dict[Dir, Dir] = {-1j: 1j, 1: -1j, 1j: 1j, -1: -1j}
        if curve == "/":
            self.dir *= CURVE[self.dir]
        else:  # \\
            self.dir *= -CURVE[self.dir]

    def is_crashing(self, other: Cart) -> bool:
        return self.pos == other.pos

    def __str__(self) -> str:
        return f"{int(self.pos.real)},{int(self.pos.imag)}"


def create_grid(data: str) -> tuple[Grid, list[Cart]]:
    CARTS: dict[str, Dir] = {"v": 1j, "^": -1j, "<": -1, ">": 1}
    grid = {}
    carts = []

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c in " -|":
                continue

            pos = x + y*1j
            if c in CARTS:
                carts.append(Cart(pos, CARTS[c]))
            else:  # + \ /
                grid[pos] = c

    return grid, carts


@timed()
def crash_test(grid: Grid, carts: list[Cart]) -> tuple[str, str]:
    crashed_carts: list[Cart] = []
    for _ in range(10**6):
        if len(carts) == 1:
            break
        carts.sort(key=lambda x: (x.pos.imag, x.pos.real))
        for cart in carts.copy():
            if cart.pos not in grid:
                cart.move()
            elif grid[cart.pos] == "+":
                cart.turn()
                cart.move()
            else:  # curve
                cart.take_curve(grid[cart.pos])
                cart.move()

            # check for crash
            for other_cart in carts:
                if other_cart == cart:
                    continue
                if cart.is_crashing(other_cart):
                    crashed_carts.extend([cart, other_cart])
                    carts.remove(cart)
                    carts.remove(other_cart)
                    break
    else:
        raise ValueError("Max iterations reached.")

    assert len(crashed_carts) > 0
    return str(crashed_carts[0]), str(carts[0])


def main() -> None:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    grid, carts = create_grid(data)
    p1, p2 = crash_test(grid, carts)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
