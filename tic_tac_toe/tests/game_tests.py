import unittest

from tic import game
from tic.exceptions import IllegalMoveError, ImpossibleGameError


class GameTest(unittest.TestCase):

    def setUp(self):
        self.game = game.Game(lines=3, columns=3)

    def test_creating_invalid_game(self):
        self.assertRaises(ImpossibleGameError, game.Game, 0, 10)
        self.assertRaises(ImpossibleGameError, game.Game, 10, 0)
        self.assertRaises(ImpossibleGameError, game.Game, -1, 0)

    def test_init_state(self):
        state = [
            "...",
            "...",
            "...",
        ]
        self.assertListEqual(self.game.state, state)

    def test_make_move(self):
        state = [
            "...",
            ".x.",
            "...",
        ]
        self.game.make_move(2, 2)
        self.assertListEqual(self.game.state, state)

    def test_wrong_move(self):
        state = [
            "...",
            "...",
            "...",
        ]

        with self.assertRaises(IllegalMoveError) as ctx:
            self.game.make_move(3, 4)
        self.assertListEqual(self.game.state, state)
        self.assertEqual(str(ctx.exception), "Value is outside of the box.")

        self.game.make_move(2, 2)
        with self.assertRaises(IllegalMoveError) as ctx:
            self.game.make_move(2, 2)
        self.assertEqual(str(ctx.exception), "Place is already taken.")
