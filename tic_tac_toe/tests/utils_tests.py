from unittest import TestCase

from tic import utils


class StatesCacheTest(TestCase):

    def setUp(self):
        self.cache = utils.StatesCache()

    def test_assignment_with_equal_state(self):
        states = [
            ([".x.", "x..", ".oo"], True),
            (["..o", "x.o", ".x."], True)
        ]
        o1, o2 = object(), object()
        self.cache[states[0]] = o1
        self.cache[states[1]] = o2
        self.assertEqual(self.cache[states[0]], o2)
        self.assertEqual(self.cache[states[1]], o2)

    def test_equal_states(self):
        states = [
            [".x.",
             "x..",
             ".oo"],
            ["..o",
             "x.o",
             ".x."],
            ["oo.",
             "..x",
             ".x."],
            [".x.",
             "o.x",
             "o.."],

            [".x.",
             "..x",
             "oo."],
            ["o..",
             "o.x",
             ".x."],
            [".oo",
             "x..",
             ".x."],
            [".x.",
             "x.o",
             "..o"]
        ]
        tmp = self.cache[(states[0], True)] = object()
        for state in states[1:]:
            self.assertEqual(self.cache[(state, True)], tmp, state)
            with self.assertRaises(KeyError):
                self.cache[(state, False)]

    def test_all_equivalent_states(self):
        state = (["ab", "cd"], True)
        possible = {
            ("abcd", True),
            ("bdac", True),
            ("dcba", True),
            ("cadb", True),
            ("badc", True),
            ("dbca", True),
            ("cdab", True),
            ("acbd", True),
        }
        result = self.cache.all_equivalent_states(state)
        self.assertSetEqual(possible, set(result))


class RotateTest(TestCase):

    def test_rotate_3x3(self):
        state = ["ab1", "cd2", "ef3"]
        self.assertListEqual(utils.rotate(state), ["eca", "fdb", "321"])

    def test_rotate_2x3(self):
        state = ["ab", "cd", "ef"]
        self.assertListEqual(utils.rotate(state), ["eca", "fdb"])

    def test_rotate_2x2(self):
        state = ["ab", "cd"]
        self.assertListEqual(utils.rotate(state), ["ca", "db"])

    def test_back_rotate_3x3(self):
        state = ["eca", "fdb", "321"]
        self.assertListEqual(utils.back_rotate(state), ["ab1", "cd2", "ef3"])

    def test_back_rotate_2x3(self):
        state = ["eca", "fdb"]
        self.assertListEqual(utils.back_rotate(state), ["ab", "cd", "ef"])

    def test_back_rotate_2x2(self):
        state = ["ca", "db"]
        self.assertListEqual(utils.back_rotate(state), ["ab", "cd"])


class ShringTest(TestCase):

    def test_shrink_2_types(self):
        line = "....xx"
        self.assertListEqual(utils.shrink(line), [('.', 4), ('x', 2)])

    def test_shrink_1_types(self):
        line = "...."
        self.assertListEqual(utils.shrink(line), [('.', 4)])

    def test_shrink_xox_pattern(self):
        line = "xoxoxoxo"
        expected = [('x', 1), ('o', 1), ('x', 1), ('o', 1), ('x', 1), ('o', 1),
                    ('x', 1), ('o', 1)]
        self.assertListEqual(utils.shrink(line), expected)

    def test_empty_line(self):
        self.assertRaises(IndexError, utils.shrink, '')
