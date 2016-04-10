import unittest
from unittest import mock

from tic import ai
from tic.game import Game
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


class HeuristicAITest(unittest.TestCase):

    def setUp(self):
        self.game = Game(5, 6, 4)
        self.ai = ai.HeuristicAI(self.game, 'o')

    def test_score_game_over(self):
        state = [
            '....x',
            '.xox.',
            '.ox..',
            '.x.o.',
            'o....',
        ]
        score = self.ai.score(depth=0, ai_move=False, state=state)
        self.assertEqual(score, -10000)
        score = self.ai.score(depth=0, ai_move=True, state=state)
        self.assertEqual(score, -10000)

    def test_score_3_with_open_ends(self):
        self.game._state = [
            ['.', '.', '.', '.', '.'],
            ['.', 'x', 'o', 'x', '.'],
            ['.', 'o', 'x', '.', '.'],
            ['.', 'x', '.', 'o', '.'],
            ['.', '.', '.', '.', '.'],
        ]
        score = self.ai.score(depth=0, ai_move=True, state=self.game.state)
        self.assertEqual(score, -2998)
        score = self.ai.score(depth=0, ai_move=False, state=self.game.state)
        self.assertEqual(score, -2998)

    def test_score_one_better_state(self):
        self.game._state = [
            ['.', '.', '.', '.', '.'],
            ['.', 'x', '.', 'x', '.'],
            ['.', 'o', 'o', '.', '.'],
            ['.', 'o', 'x', '.', '.'],
            ['.', '.', '.', '.', '.'],
        ]
        score = self.ai.score(depth=0, ai_move=True, state=self.game.state)
        self.assertEqual(score, 2002)
        score = self.ai.score(depth=0, ai_move=False, state=self.game.state)
        self.assertEqual(score, 2)


class GetHeuristicAIClassTest(unittest.TestCase):

    def test_get_heuristic_ai_class(self):
        ai_class = ai.get_heuristic_ai_class(20)
        self.assertEqual(ai_class.max_depth, 20)
        ai_class = ai.get_heuristic_ai_class(7)
        self.assertEqual(ai_class.max_depth, 7)
        self.ai = ai_class(mock.MagicMock(), 'o')
        self.assertEqual(self.ai.max_depth, 7)
