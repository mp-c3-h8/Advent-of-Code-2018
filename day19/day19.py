import os.path
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'device'))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa
from device import Device  # noqa


def run_program(data: str) -> tuple[int, int]:
    device = Device(6)
    for line in data.splitlines():
        if line.startswith("#ip"):
            _, ip = line.split(" ")
            device.set_pointer(int(ip))
        else:
            op, a, b, c = line.split(" ")
            device.add_instruction(op, (int(a), int(b), int(c)))
    device.run()
    p1 = device.registers[0]

    # part 2
    device.reset_registers()
    device.registers[0] = 1
    # device.run()
    # p2 = device.registers[0]
    return p1, -1


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    p1, p2 = run_program(data)
    print("Part1 :", p1)
    print("Part2 :", p2)


if __name__ == "__main__":
    main()
