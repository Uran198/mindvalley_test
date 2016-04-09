from .utils import StatesCache

from .exceptions import NoLegalMoveError


def get_default_ai(game, ai_pieces):
    return SimpleAI(game, ai_pieces)


class BasicAI:

    def __init__(self, game, pieces):
        self._game = game
        self._pieces = pieces

    def next_move(self):
        raise NotImplementedError


class SimpleAI(BasicAI):

    def next_move(self):
        for i, row in enumerate(self._game.state):
            for j, val in enumerate(row):
                if val == self._game.empty_place:
                    return (i, j)
        raise NoLegalMoveError("AI found no legal move to make.")


class MinimaxAI(BasicAI):
    max_score = 10000
    min_score = -10000

    def __init__(self, *args, **kwargs):
        self._cache = StatesCache()
        super(MinimaxAI, self).__init__(*args, **kwargs)

    def next_move(self):
        if ''.join(self._game.state).count(self._game.empty_place) == 0:
            raise NoLegalMoveError("AI found no legal move to make.")
        self._cache = StatesCache()
        score, move = self.minimax(self._game.state, True, 0)
        print("Score, Move", score, move)
        return move

    def score(self, state, depth):
        winner = self._game.get_winner(state)
        if winner is None:
            score = 0
        elif winner == "ai":
            score = self.max_score - depth
        else:
            score = self.min_score + depth
        return score

    def minimax(self, state, is_max, depth):
        depth += 1
        if self._game.is_game_over(state):
            return (self.score(state, depth), (-1, -1))

        try:
            return self._cache[(state, is_max)]
        except KeyError:
            pass

        scoremoves = []

        for i, row in enumerate(state):
            for j, val in enumerate(row):
                if val != self._game.empty_place:
                    continue
                piece = self._pieces if is_max else self._game.player_piece
                next_state = self._game.get_next_state(state, i, j, piece)
                sm = (self.minimax(next_state, not is_max, depth)[0], (i, j))
                scoremoves.append(sm)

        if is_max:
            result = max(scoremoves, key=lambda x: x[0])
        else:
            result = min(scoremoves, key=lambda x: x[0])
        self._cache[(state, is_max)] = result
        return result
