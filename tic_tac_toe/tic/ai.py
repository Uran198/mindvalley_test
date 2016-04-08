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

    def __init__(self, *args, **kwargs):
        self._cache = {}
        super(MinimaxAI, self).__init__(*args, **kwargs)

    def next_move(self):
        if ''.join(self._game.state).count(self._game.empty_place) == 0:
            raise NoLegalMoveError("AI found no legal move to make.")
        score, move = self.minimax(self._game.state, True)
        return move

    def score(self, state):
        winner = self._game.get_winner(state)
        if winner is None:
            score = 0
        elif winner == "ai":
            score = 1
        else:
            score = -1
        return score

    def minimax(self, state, is_max):
        if self._game.is_game_over(state):
            return (self.score(state), (-1, -1))

        if (''.join(state), is_max) in self._cache:
            return self._cache[(''.join(state), is_max)]

        scoremoves = []

        for i, row in enumerate(state):
            for j, val in enumerate(row):
                if val != self._game.empty_place:
                    continue
                piece = self._pieces if is_max else self._game.player_piece
                next_state = self._game.get_next_state(state, i, j, piece)
                scoremoves.append(
                    (self.minimax(next_state, not is_max)[0], (i, j))
                )

        if is_max:
            result = max(scoremoves, key=lambda x: x[0])
        else:
            result = min(scoremoves, key=lambda x: x[0])
        self._cache[(''.join(state), is_max)] = result
        return result
