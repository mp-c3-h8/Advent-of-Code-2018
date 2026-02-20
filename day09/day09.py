import os.path
import os
from timeit import default_timer as timer
from collections import deque, Counter


def play_marbles(num_players: int, num_marbles: int) -> int:
    marbles = deque([0])
    scores: Counter[int] = Counter()  # last player is player 0
    for marble in range(1, num_marbles+1):
        if marble % 23 == 0:
            marbles.rotate(7)
            scores[marble % num_players] += marble + marbles.pop()
            marbles.rotate(-1)
        else:
            marbles.rotate(-1)
            marbles.append(marble)
    winner = scores.most_common(1)
    return winner[0][1] if winner else 0


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

split = data.split(" ")
num_players = int(split[0])
num_marbles = int(split[-2])

print("Part 1:", play_marbles(num_players, num_marbles))
print("Part 2:", play_marbles(num_players, num_marbles*100))


e = timer()
print(f"time: {e-s}")
