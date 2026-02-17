import os.path
import os
from collections import Counter, defaultdict
from datetime import datetime
from dataclasses import dataclass


@dataclass(slots=True, order=True)
class Observation:
    dt: datetime
    guard_id: int
    type: int  # 0: guard begins shift, 1 = falls asleep, 2 = wakes up


def parse(data: str) -> list[Observation]:
    res = []
    for line in data.splitlines():
        dt_str, rest = line.split("] ")
        info = rest.split(" ")
        guard_id = int(info[1][1:]) if info[0] == "Guard" else -1
        type = 0 if info[0] == "Guard" else 1 if info[0] == "falls" else 2
        dt = datetime.fromisoformat(dt_str[1:])
        obs = Observation(dt, guard_id, type)
        res.append(obs)
    res.sort()
    return res


def strategies(observations: list[Observation]) -> tuple[int, int]:
    guards: defaultdict[int, Counter] = defaultdict(Counter)  # guard_id: counter(minutes)
    curr_guard = -1
    for i, obs in enumerate(observations):
        if obs.type == 0:
            curr_guard = obs.guard_id
        elif obs.type == 2:  # wakes up
            assert observations[i-1].type == 1  # "falling asleep" must be before "waking up"
            min_start = observations[i-1].dt.minute
            min_delta = round((obs.dt - observations[i-1].dt).seconds / 60)
            for m in range(min_start, min_start + min_delta):
                guards[curr_guard][m % 60] += 1

    strategy_1 = max(guards.items(), key=lambda x: x[1].total())
    p1 = strategy_1[0] * strategy_1[1].most_common(1)[0][0]

    strategy_2 = max(guards.items(), key=lambda x: x[1].most_common(1)[0][1])
    p2 = strategy_2[0] * strategy_2[1].most_common(1)[0][0]
    return p1, p2


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

observations = parse(data)
p1, p2 = strategies(observations)
print("Part 1:", p1)
print("Part 2:", p2)
