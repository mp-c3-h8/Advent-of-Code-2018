import os.path
import os
from abc import ABC
from utils import timed
from collections import Counter
from heapq import heapify, heappop, heappush
from copy import deepcopy

type Pos = tuple[int, int]  # (y,x) y downwards
type Dir = tuple[int, int]
type Battlefield = set[Pos]
type Item = tuple[int, Pos, Pos]

DIRS: list[Dir] = [(-1, 0), (0, -1), (1, 0), (0, 1)]


class Unit(ABC):
    __slots__ = ["pos", "hp", "is_dead", "power"]

    def __init__(self, pos: Pos) -> None:
        self.pos = pos
        self.hp: int = 200
        self.power: int = 3
        self.is_dead: bool = False

    def is_enemy(self, other: Unit) -> bool:
        return not isinstance(other, self.__class__)


class Elf(Unit):
    def __init__(self, pos: Pos) -> None:
        super().__init__(pos)


class Goblin(Unit):
    def __init__(self, pos: Pos) -> None:
        super().__init__(pos)


def unit_factory(type: str, pos: Pos) -> Unit:
    return Goblin(pos) if type == "G" else Elf(pos)


def setup(data: str) -> tuple[Battlefield, list[Unit]]:
    battlefield = set()
    units = []

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c in "# ":
                continue
            pos = (y, x)
            if c in "EG":
                units.append(unit_factory(c, pos))
            battlefield.add(pos)

    return battlefield, units


def move_to_enemy(unit: Unit, battlefield: Battlefield, pos_to_unit: dict[Pos, Unit]) -> Pos | None:
    global DIRS
    # chosen priority    steps -> pos -> first_step    takes care of movement rules
    init: Item = (0, unit.pos, unit.pos)
    q: list[Item] = [init]
    heapify(q)
    shortest_path: dict[Pos, int] = {}
    done: set[Pos] = set()

    while q:
        steps, pos, first_step = heappop(q)

        if pos in done:
            continue
        done.add(pos)

        for d in DIRS:
            new_pos = (pos[0]+d[0], pos[1]+d[1])

            if new_pos in done:
                continue
            if new_pos not in battlefield:
                continue
            if new_pos in pos_to_unit:
                if pos_to_unit[new_pos].is_enemy(unit):
                    return first_step
                else:
                    continue

            new_steps = steps+1
            # important for considering all shortest paths!
            # usually its " <= new_steps"
            if new_pos in shortest_path and shortest_path[new_pos] < new_steps:
                continue
            shortest_path[new_pos] = new_steps
            first_step = new_pos if steps == 0 else first_step
            heappush(q, (new_steps, new_pos, first_step))

    return None


def get_enemies_in_range(unit: Unit, pos_to_unit: dict[Pos, Unit]) -> list[Unit]:
    global DIRS
    enemies_in_range: list[Unit] = []
    for d in DIRS:
        adj = (unit.pos[0] + d[0], unit.pos[1] + d[1])
        if adj in pos_to_unit and pos_to_unit[adj].is_enemy(unit):
            enemies_in_range.append(pos_to_unit[adj])
    return enemies_in_range


def battle(battlefield: Battlefield, units: list[Unit], empower_elves: bool = False) -> int:
    global DIRS
    unit_count: Counter[type[Unit]] = Counter(u.__class__ for u in units)
    pos_to_unit: dict[Pos, Unit] = {u.pos: u for u in units}

    for i in range(1, 10**6):
        units.sort(key=lambda u: u.pos)
        for unit in units.copy():

            # already dead? (we work on a copy)
            if unit.is_dead:
                continue

            # need to move?
            enemies_in_range = get_enemies_in_range(unit, pos_to_unit)
            if len(enemies_in_range) == 0:
                new_pos = move_to_enemy(unit, battlefield, pos_to_unit)
                if new_pos is not None:
                    del pos_to_unit[unit.pos]
                    pos_to_unit[new_pos] = unit
                    unit.pos = new_pos
                    enemies_in_range = get_enemies_in_range(unit, pos_to_unit)
                elif any(count == 0 for count in unit_count.values()):
                    remaining_hp = sum(u.hp for u in units)
                    return remaining_hp*(i-1)

            # can attack?
            if len(enemies_in_range) > 0:
                enemies_in_range.sort(key=lambda u: (u.hp, u.pos))
                enemy = enemies_in_range[0]
                enemy.hp -= unit.power
                if enemy.hp <= 0:
                    enemy.is_dead = True
                    del pos_to_unit[enemy.pos]
                    unit_count[enemy.__class__] -= 1
                    units.remove(enemy)

                    # part 2: game over if elf dies
                    if empower_elves and isinstance(enemy, Elf):
                        return -1

    else:
        raise ValueError("Max iterations reached.")


@timed("Part 2")
def empower_elves(battlefield: Battlefield, units: list[Unit]) -> int:

    for power in range(4, 10**6):
        new_units = deepcopy(units)
        for unit in new_units:
            if isinstance(unit, Elf):
                unit.power = power
        outcome = battle(battlefield, new_units, True)
        if outcome != -1:
            return outcome
    else:
        raise ValueError("Max iterations reached.")


def main() -> None:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    battlefield, units = setup(data)
    print("Part 1:", battle(battlefield, deepcopy(units)))
    print("Part 2:", empower_elves(battlefield, units))


if __name__ == "__main__":
    main()
