import numpy as np
from scipy.ndimage import convolve
import os.path
import os


def parse(data: str) -> tuple[np.ndarray, np.ndarray]:
    initial, rules = data.split("\n\n")
    *rest, init = initial.split(" ")
    pots = np.array([1 if c == "#" else 0 for c in init])
    KERNEL = np.array([2**(4-i) for i in range(5)], dtype=int)
    lookup = np.zeros(KERNEL.sum()+1, dtype=int)

    for rule in rules.splitlines():
        cond, res = rule.split(" => ")
        if res == ".":
            continue
        configuration = np.array([1 if c == "#" else 0 for c in cond], dtype=int)
        idx = KERNEL @ configuration
        lookup[idx] = 1

    return pots, lookup


def conway(pots: np.ndarray, lookup: np.ndarray, steps: int) -> int:
    KERNEL = np.array([2**i for i in range(5)], dtype=int)  # reverse
    for _ in range(steps):
        pots = np.pad(pots, 1)
        conv = convolve(pots, KERNEL, mode="constant")
        pots = lookup[conv]  # type: ignore

    idx = np.arange(-steps, len(pots)-steps)
    return np.dot(pots, idx)


def main() -> None:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    pots, lookup = parse(data)
    p1 = conway(pots, lookup, 20)
    print("Part 1:", p1)

    # zeroes in the middle grow
    print(f"500 steps: {conway(pots, lookup, 500)}, 5000 steps: {conway(pots, lookup, 5000)}")
    # 50 billion has 10 zeroes
    zeroes = 10
    p2 = "21" + "0"*(zeroes-1) + "61"
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
