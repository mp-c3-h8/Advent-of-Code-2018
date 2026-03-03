import os.path
import os
import sys
import re
from enum import Enum
from copy import deepcopy

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

type AttackType = str


class Team(Enum):
    IMMUNE_SYSTEM = 0
    INFECTION = 1


class Units:
    __slots__ = ["team", "count", "hp", "attack_damage", "attack_type",
                 "initiative", "is_dead", "weaknesses", "immunities"]

    def __init__(self, team: Team, count: int, hp: int, attack_damage: int, attack_type: AttackType, initiative: int) -> None:
        self.team: Team = team
        self.count: int = count
        self.hp: int = hp
        self.attack_damage: int = attack_damage
        self.attack_type: AttackType = attack_type
        self.initiative: int = initiative

        self.is_dead: bool = False
        self.weaknesses: set[AttackType] = set()
        self.immunities: set[AttackType] = set()

    @property
    def effective_power(self) -> int:
        return self.count * self.attack_damage

    def damage_to_units(self, other_units: Units) -> int:
        if self.attack_type in other_units.immunities:
            return 0
        if self.attack_type in other_units.weaknesses:
            return 2*self.effective_power
        return self.effective_power


def create_units(data: str) -> list[Units]:
    all_units: list[Units] = []
    r_digits = re.compile(r"-?\d+")
    r_attack_type = re.compile(r"\w+(?= damage)")
    r_parentheses = re.compile(r"\((.*)\)")
    for army_data, team in zip(data.split("\n\n"), Team):
        for units_data in army_data.splitlines()[1:]:
            count, hp, attack_damage, initiative = map(int, r_digits.findall(units_data))
            attack_type_match = r_attack_type.search(units_data)
            assert attack_type_match
            attack_type = attack_type_match.group(0)
            units = Units(team, count, hp, attack_damage, attack_type, initiative)

            in_paren = r_parentheses.findall(units_data)
            if len(in_paren) == 1:
                conditions = in_paren[0].split("; ")
                for cond in conditions:
                    if cond.startswith("weak to"):
                        types = cond[8:].split(", ")
                        units.weaknesses.update(types)
                    elif cond.startswith("immune to "):
                        types = cond[10:].split(", ")
                        units.immunities.update(types)
            all_units.append(units)

    return all_units


def sim_combat(all_units: list[Units], boosted: bool = False) -> int:
    population = sum(u.count for u in all_units)
    for i in range(1, 10**6):
        # PHASE: target selection
        selections: list[tuple[Units, Units]] = []  # (attacker,defender)
        selected: set[Units] = set()
        # who chooses first?
        all_units.sort(key=lambda u: (u.effective_power, u.initiative), reverse=True)
        for attacker in all_units:
            # who to attack?
            targets = sorted((defender for defender in all_units if defender.team != attacker.team and defender not in selected and attacker.damage_to_units(defender) != 0),
                             key=lambda defender: (attacker.damage_to_units(defender), defender.effective_power, defender.initiative), reverse=True)
            if len(targets) == 0:
                continue
            target_chosen = targets[0]
            selected.add(target_chosen)
            selections.append((attacker, target_chosen))

        # PHASE: attacking
        # who attacks first?
        selections.sort(key=lambda s: s[0].initiative, reverse=True)
        for attacker, defender in selections:
            if attacker.is_dead or defender.is_dead:
                continue
            units_lost = attacker.damage_to_units(defender) // defender.hp
            defender.count -= units_lost
            if defender.count <= 0:
                defender.count = 0
                defender.is_dead = True
                all_units.remove(defender)

        # did combat progress?
        new_population = sum(u.count for u in all_units)
        if new_population == population:
            # do we have immune vs. immune? or stalemate?
            remaining_teams: set[Team] = set(unit.team for unit in all_units)

            if len(remaining_teams) > 1:
                return -1

            # part 2
            winner = remaining_teams.pop()
            if boosted and winner == Team.INFECTION:
                return -1
            return population

        population = new_population
    else:
        raise ValueError("Max iterations reached.")


def boost_reindeer(all_units: list[Units]) -> int:
    for boost in range(1, 10**6):
        new_units = deepcopy(all_units)
        for units in new_units:
            if units.team == Team.IMMUNE_SYSTEM:
                units.attack_damage += boost

        outcome = sim_combat(new_units, True)
        if outcome != -1:
            return outcome
    else:
        raise ValueError("Max iterations reached.")


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    all_units = create_units(data)
    p1 = sim_combat(deepcopy(all_units))
    print("Part 1:", p1)

    p2 = boost_reindeer(all_units)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
