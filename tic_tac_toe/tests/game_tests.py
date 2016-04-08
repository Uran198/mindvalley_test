import unittest
import unittest.mock as mock

from tic import game
from tic.exceptions import (
    IllegalMoveError, ImpossibleGameError, InvalidAIError
)


class GameTest(unittest.TestCase):

    def setUp(self):
        self.ai_class = mock.MagicMock()
        self.ai = mock.Mock()
        self.ai_class.return_value = self.ai
        self.ai.next_move.return_value = (2, 2)

        self.game = game.Game(lines=3, columns=3)
        self.game.start(ai_class=self.ai_class, player_first=True)

    def test_ai_piece(self):
        self.assertEqual(self.game.ai_piece, 'o')

    def test_player_piece(self):
        self.assertEqual(self.game.player_piece, 'x')

    def test_empty_place(self):
        self.assertEqual(self.game.empty_place, '.')

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
            "..o",
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

    def test_get_winner(self):
        self.assertEqual(self.game.get_winner(), None)
        player_winning = [
            ["x..",
             ".x.",
             "..x"],
            ["xxx",
             "...",
             "..."],
            [".x.",
             ".x.",
             ".x."],
        ]
        ai_winning = [
            ["..o",
             ".o.",
             "o.."],
            ["o..",
             ".o.",
             "..o"],
            ["ooo",
             "...",
             "..."],
            [".o.",
             ".o.",
             ".o."],
        ]
        for state in player_winning:
            self.game._state = state
            self.assertEqual(self.game.get_winner(), "player")

        for state in ai_winning:
            self.game._state = state
            self.assertEqual(self.game.get_winner(), "ai", state)

    def test_start(self):
        self.ai_class.reset_mock()
        self.ai.next_move.return_value = (2, 2)
        self.game.start(ai_class=self.ai_class, player_first=False)
        self.assertListEqual(self.game.state, ['...', '...', '..o'])
        self.ai_class.assert_called_once_with(self.game, 'o')
        self.ai.next_move.assert_called_once_with()

        self.game.start(ai_class=self.ai_class, player_first=True)
        self.assertListEqual(self.game.state, ['...', '...', '...'])
        self.ai_class.assert_called_with(self.game, 'o')
        self.ai.next_move.assert_has_calls([])

    @mock.patch('tic.game.get_default_ai', create=True)
    def test_start_no_ai(self, get_default_ai):
        get_default_ai.return_value = self.ai
        self.game.start(player_first=False)
        get_default_ai.assert_called_once_with(self.game, 'o')
        self.assertListEqual(self.game.state, ['...', '...', '..o'])

        self.game.start(player_first=True)
        self.assertListEqual(self.game.state, ['...', '...', '...'])

    def test_invalid_ai(self):
        self.ai.next_move.return_value = (4, 2)
        with self.assertRaises(InvalidAIError) as ctx:
            self.game.start(ai_class=self.ai_class, player_first=False)
        self.assertEqual(str(ctx.exception),
                         "AI tried to make a move outside the board.")
        self.game._state = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]
        self.ai.next_move.return_value = (0, 2)
        with self.assertRaises(InvalidAIError) as ctx:
            self.game.make_move(1, 3)
        self.assertEqual(str(ctx.exception),
                         "AI tried to place piece in already occupied place.")

    def test_make_move_ai_move(self):
        self.ai_class.reset_mock()
        self.game.start(ai_class=self.ai_class, player_first=True)
        self.game.make_move(1, 2)
        self.ai_class.assert_called_once_with(self.game, 'o')
        self.ai.next_move.assert_called_once_with()
