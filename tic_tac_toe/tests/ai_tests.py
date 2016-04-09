import unittest
from unittest import mock

from tic import ai
from tic.exceptions import NoLegalMoveError


class DefaultAITest(unittest.TestCase):

    def test_get_default_ai(self):
        game = mock.Mock()
        result = ai.get_default_ai(game, 'o')
        self.assertIsInstance(result, ai.SimpleAI)
        self.assertEqual(result._game, game)
        self.assertEqual(result._pieces, 'o')


class BasicAITest(unittest.TestCase):

    def setUp(self):
        self.game = mock.Mock()
        self.game.state = [
            '...',
            '...',
            '...',
        ]

        self.ai_class = ai.BasicAI

    def test_init(self):
        self.ai_class(self.game, 'o')
        self.assertRaises(TypeError, self.ai_class)
        self.assertRaises(TypeError, self.ai_class, self.game)

    def test_next_move(self):
        ai = self.ai_class(self.game, 'o')
        self.assertRaises(NotImplementedError, ai.next_move)


class SimpleAITest(unittest.TestCase):

    def setUp(self):
        self.game = mock.Mock()
        self.game.state = [
            '...',
            '...',
            '...',
        ]
        self.game.empty_place = '.'

        self.ai = ai.SimpleAI(self.game, 'o')

    def test_next_move(self):
        self.assertEqual(self.ai.next_move(), (0, 0))

    def test_next_move_without_legal_moves(self):
        self.game.empty_place = 't'
        self.assertRaises(NoLegalMoveError, self.ai.next_move)


class MinimaxAITest(unittest.TestCase):

    def setUp(self):
        self.game = mock.Mock()
        self.game.state = ['...']*3
        self.game.empty_place = '.'

        self.ai = ai.MinimaxAI(self.game, 'o')

    def test_no_legal_move(self):
        self.game.empty_place = 'l'
        self.assertRaises(NoLegalMoveError, self.ai.next_move)

    def test_score(self):
        self.game.get_winner = mock.Mock()
        self.game.get_winner.return_value = "ai"
        self.assertEqual(self.ai.score("fake", 0), self.ai.max_score)
        self.game.get_winner.return_value = "player"
        self.assertEqual(self.ai.score("fake", 0), self.ai.min_score)
        self.game.get_winner.return_value = None
        self.assertEqual(self.ai.score("fake", 0), 0)

    def test_next_move(self):
        from tic.game import Game
        self.game = Game(3, 3)
        self.ai = ai.MinimaxAI(self.game, 'o')
        self.assertIn(self.ai.next_move(),
                      [(0, 0), (1, 1), (2, 2), (0, 2), (2, 0)])
        self.game._state = [
            ['o', 'x', '.'],
            ['.', '.', '.'],
            ['.', '.', '.']
        ]
        self.assertIn(self.ai.next_move(),
                      [(1, 1), (2, 0), (1, 0)])
        self.game._state = [
            ['o', '.', 'x'],
            ['.', '.', '.'],
            ['.', '.', '.']
        ]
        self.assertIn(self.ai.next_move(),
                      [(1, 1), (2, 0), (1, 0)])
