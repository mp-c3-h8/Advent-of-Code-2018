import os.path
import os
from timeit import default_timer as timer
import numpy as np
import re


def message_in_the_sky(data: str) -> tuple[np.ndarray, int]:
    regexp = re.compile(r"-?\d+")
    pos = []
    vel = []
    for line in data.splitlines():
        px, py, vx, vy = map(int, regexp.findall(line))
        pos.append([px, py])
        vel.append([vx, vy])

    positions = np.array(pos, dtype=int)
    velocities = np.array(vel, dtype=int)
    num_points = len(pos)

    for i in range(1, 10**6):
        positions += velocities
        x_max, y_max = np.max(positions, axis=0)
        x_min, y_min = np.min(positions, axis=0)

        area = (x_max-x_min+1) * (y_max-y_min+1)
        # 30% of the image should be filled
        # faster assuming the bounding box / area is unimodal:
        # gradient descent, bisection etc
        if num_points / area > 0.3:
            break

    else:
        raise ValueError("Message not found.")
    return positions, i


def print_message(positions: np.ndarray) -> None:
    x_max, y_max = np.max(positions, axis=0)
    x_min, y_min = np.min(positions, axis=0)

    points = set((x, y) for x, y in positions)
    for y in range(y_min, y_max+1):
        for x in range(x_min, x_max+1):
            print("█" if (x, y) in points else " ", end="")
        print()


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

message, seconds = message_in_the_sky(data)
print("Part 1:")
print_message(message)
print("Part 2:", seconds)


e = timer()
print(f"time: {e-s}")
