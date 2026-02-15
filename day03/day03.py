import os.path
import os
import numpy as np
import re


def parse(data: str) -> list[list[int]]:
    regexp = re.compile(r"\d+")
    return [[*map(int, regexp.findall(line))] for line in data.splitlines()]


def claim_fabric(claims: list[list[int]]) -> np.ndarray:
    fabric = np.zeros((1000, 1000), dtype=np.int8)
    for idx, ox, oy, w, h in claims:
        fabric[oy:oy+h, ox:ox+w] += 1
    return fabric


def intact_claim(claims: list[list[int]], fabric: np.ndarray) -> int:
    for idx, ox, oy, w, h in claims:
        area = w*h
        if fabric[oy:oy+h, ox:ox+w].sum() == area:
            return idx
    else:
        raise ValueError("No intact claim found.")


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

claims = parse(data)
fabric = claim_fabric(claims)
print("Part 1:", (fabric > 1).sum())
print("Part 1:", intact_claim(claims, fabric))
