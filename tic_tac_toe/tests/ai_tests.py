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
            ['.', '.', '.'],
            ['.', '.', '.'],
            ['.', '.', '.'],
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
            ['.', '.', '.'],
            ['.', '.', '.'],
            ['.', '.', '.'],
        ]
        self.game.empty_place = '.'

        self.ai = ai.SimpleAI(self.game, 'o')

    def test_next_move(self):
        self.assertEqual(self.ai.next_move(), (0, 0))

    def test_next_move_without_legal_moves(self):
        self.game.empty_place = 't'
        self.assertRaises(NoLegalMoveError, self.ai.next_move)
