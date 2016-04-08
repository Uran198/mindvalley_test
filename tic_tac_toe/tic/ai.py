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
