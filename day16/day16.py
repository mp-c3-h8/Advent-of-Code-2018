import os.path
import os
from utils import timed
from typing import Callable
import re
from collections import defaultdict

type Register = int
type Registers = list[int]
type OpCode = int
type Operation = Callable[[Registers, int, int, int]]


def addr(reg: Registers, a: int, b: int, c: int) -> Registers:
    reg[c] = reg[a] + reg[b]
    return reg


def addi(reg: Registers, a: int, b: int, c: int) -> Registers:
    reg[c] = reg[a] + b
    return reg


def mulr(reg: Registers, a: int, b: int, c: int) -> Registers:
    reg[c] = reg[a] * reg[b]
    return reg


def muli(reg: Registers, a: int, b: int, c: int) -> Registers:
    reg[c] = reg[a] * b
    return reg


def banr(reg: Registers, a: int, b: int, c: int) -> Registers:
    reg[c] = reg[a] & reg[b]
    return reg


def bani(reg: Registers, a: int, b: int, c: int) -> Registers:
    reg[c] = reg[a] & b
    return reg


def borr(reg: Registers, a: int, b: int, c: int) -> Registers:
    reg[c] = reg[a] | reg[b]
    return reg


def bori(reg: Registers, a: int, b: int, c: int) -> Registers:
    reg[c] = reg[a] | b
    return reg


def setr(reg: Registers, a: int, b: int, c: int) -> Registers:
    reg[c] = reg[a]
    return reg


def seti(reg: Registers, a: int, b: int, c: int) -> Registers:
    reg[c] = a
    return reg


def gtir(reg: Registers, a: int, b: int, c: int) -> Registers:
    reg[c] = 1 if a > reg[b] else 0
    return reg


def gtri(reg: Registers, a: int, b: int, c: int) -> Registers:
    reg[c] = 1 if reg[a] > b else 0
    return reg


def gtrr(reg: Registers, a: int, b: int, c: int) -> Registers:
    reg[c] = 1 if reg[a] > reg[b] else 0
    return reg


def eqir(reg: Registers, a: int, b: int, c: int) -> Registers:
    reg[c] = 1 if a == reg[b] else 0
    return reg


def eqri(reg: Registers, a: int, b: int, c: int) -> Registers:
    reg[c] = 1 if reg[a] == b else 0
    return reg


def eqrr(reg: Registers, a: int, b: int, c: int) -> Registers:
    reg[c] = 1 if reg[a] == reg[b] else 0
    return reg


OPERATIONS: list[Operation] = [
    addr, addi, mulr, muli, banr, bani, borr, bori,
    setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr
]


def solve(data: str) -> tuple[int, int]:
    global OPERATIONS
    samples, program = data.split("\n\n\n\n")
    regexp = re.compile(r"-?\d+")

    # part 1
    p1 = 0
    candidates: defaultdict[OpCode, set[Operation]] = defaultdict(set)
    for sample in samples.split("\n\n"):
        rows = sample.splitlines()
        before: Registers = [*map(int, regexp.findall(rows[0]))]
        opcode, a, b, c = [*map(int, regexp.findall(rows[1]))]
        after: Registers = [*map(int, regexp.findall(rows[2]))]
        num_valid = 0
        for operation in OPERATIONS:
            if operation(before[::], a, b, c) == after:
                num_valid += 1
                candidates[opcode].add(operation)
        p1 += num_valid >= 3

    # part 2
    operations: list[Operation] = [addr] * len(OPERATIONS)
    for _ in range(len(OPERATIONS)):
        to_add: list[tuple[OpCode, Operation]] = [(opcode, cand.pop())
                                                  for opcode, cand in candidates.items() if len(cand) == 1]
        to_remove: set[Operation] = set()
        for opcode, operation in to_add:
            operations[opcode] = operation
            to_remove.add(operation)
        for cand in candidates.values():
            cand.difference_update(to_remove)

    registers = [0, 0, 0, 0]
    for instr in program.splitlines():
        opcode, a, b, c = map(int, instr.split(" "))
        operations[opcode](registers, a, b, c)
    p2 = registers[0]

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
