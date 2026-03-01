import os.path
import os
import sys
import re
from collections import defaultdict
from typing import Callable

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'device'))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa
from device import Device  # noqa

type OpCode = int


def solve(data: str) -> tuple[int, int]:
    device = Device(4)
    samples, program = data.split("\n\n\n\n")
    regexp = re.compile(r"-?\d+")

    # part 1
    p1 = 0
    candidates: defaultdict[OpCode, set[Callable]] = defaultdict(set)
    for sample in samples.split("\n\n"):
        rows = sample.splitlines()
        before = [*map(int, regexp.findall(rows[0]))]
        opcode, a, b, c = [*map(int, regexp.findall(rows[1]))]
        after = [*map(int, regexp.findall(rows[2]))]
        num_valid = 0
        for operation in device.operations:
            device.registers = before[::]
            operation(a, b, c)
            if device.registers == after:
                num_valid += 1
                candidates[opcode].add(operation)
        p1 += num_valid >= 3

    # part 2
    operations: list[Callable] = [device.addr] * len(device.operations)  # dummy
    for _ in range(len(device.operations)):
        to_add: list[tuple[OpCode, Callable]] = [(opcode, cand.pop())
                                                 for opcode, cand in candidates.items() if len(cand) == 1]
        to_remove: set[Callable] = set()
        for opcode, operation in to_add:
            operations[opcode] = operation
            to_remove.add(operation)
        for cand in candidates.values():
            cand.difference_update(to_remove)

    device.reset()
    for instr in program.splitlines():
        opcode, a, b, c = map(int, instr.split(" "))
        operations[opcode](a, b, c)
    p2 = device.registers[0]

    return p1, p2


@timed("All")
def main() -> None:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    p1, p2 = solve(data)
    print("Part1 :", p1)
    print("Part2 :", p2)


if __name__ == "__main__":
    main()
