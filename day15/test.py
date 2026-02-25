import unittest
from copy import deepcopy

import day15


class Tests(unittest.TestCase):
    def test_ex1(self):
        data = [
            ("####### \n #.G...# \n #...EG# \n #.#.#G# \n #..G#E# \n #.....# \n #######", 27730, 4988),
            ("####### \n #E..EG# \n #.#G.E# \n #E.##E# \n #G..#.# \n #..E#.# \n #######", 39514, 31284),
            ("####### \n #E.G#.# \n #.#G..# \n #G.#.G# \n #G..#.# \n #...E.# \n #######", 27755, 3478),
            ("####### \n #.E...# \n #.#..G# \n #.###.# \n #E#G#G# \n #...#G# \n #######", 28944, 6474),
            ("######### \n #G......# \n #.E.#...# \n #..##..G# \n #...##..# \n #...#...# \n #.G...G.# \n #.....G.# \n #########", 18740, 1140),
        ]
        for inp, p1, p2 in data:
            battlefield, units = day15.setup(inp)  # type: ignore
            self.assertEqual(day15.battle(battlefield, deepcopy(units)), p1)  # type: ignore
            self.assertEqual(day15.empower_elves(battlefield, units), p2)  # type: ignore


if __name__ == "__main__":
    unittest.main()
