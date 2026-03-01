from typing import Callable

type Registers = list[int]
type Operation = Callable[[int, int, int], None]


class Device:
    __slots__ = ["registers", "operations"]

    def __init__(self, num_registers: int) -> None:
        self.registers: Registers = [0]*num_registers
        self.operations: list[Operation] = [
            self.addr, self.addi,
            self.mulr, self.muli,
            self.banr, self.bani,
            self.borr, self.bori,
            self.setr, self.seti,
            self.gtir, self.gtri, self.gtrr,
            self.eqir, self.eqri, self.eqrr
        ]

    def reset(self) -> None:
        self.registers = [0]*len(self.registers)

    def addr(self, a: int, b: int, c: int) -> None:
        self.registers[c] = self.registers[a] + self.registers[b]

    def addi(self, a: int, b: int, c: int) -> None:
        self.registers[c] = self.registers[a] + b

    def mulr(self, a: int, b: int, c: int) -> None:
        self.registers[c] = self.registers[a] * self.registers[b]

    def muli(self, a: int, b: int, c: int) -> None:
        self.registers[c] = self.registers[a] * b

    def banr(self, a: int, b: int, c: int) -> None:
        self.registers[c] = self.registers[a] & self.registers[b]

    def bani(self, a: int, b: int, c: int) -> None:
        self.registers[c] = self.registers[a] & b

    def borr(self, a: int, b: int, c: int) -> None:
        self.registers[c] = self.registers[a] | self.registers[b]

    def bori(self, a: int, b: int, c: int) -> None:
        self.registers[c] = self.registers[a] | b

    def setr(self, a: int, b: int, c: int) -> None:
        self.registers[c] = self.registers[a]

    def seti(self, a: int, b: int, c: int) -> None:
        self.registers[c] = a

    def gtir(self, a: int, b: int, c: int) -> None:
        self.registers[c] = 1 if a > self.registers[b] else 0

    def gtri(self, a: int, b: int, c: int) -> None:
        self.registers[c] = 1 if self.registers[a] > b else 0

    def gtrr(self, a: int, b: int, c: int) -> None:
        self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0

    def eqir(self, a: int, b: int, c: int) -> None:
        self.registers[c] = 1 if a == self.registers[b] else 0

    def eqri(self, a: int, b: int, c: int) -> None:
        self.registers[c] = 1 if self.registers[a] == b else 0

    def eqrr(self, a: int, b: int, c: int) -> None:
        self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0
