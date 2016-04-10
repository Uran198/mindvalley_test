from .utils import StatesCache, shrink

from .exceptions import NoLegalMoveError


def get_default_ai(game, ai_pieces):
    return SimpleAI(game, ai_pieces)


def get_heuristic_ai_class(depth):
    class HeuristicAIDepth(HeuristicAI):
        max_depth = depth
    return HeuristicAIDepth


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


class HeuristicAI(MinimaxAI):
    """
    Makes move based on heuristic positions evaluation. With the value of
    max_depth set to 4 thinks approximately for 10 seconds on the move with 5x5
    board and 4 in a row.
    """
    max_depth = 4

    def __init__(self, *args, **kwargs):
        self._score_cache = StatesCache()
        super(HeuristicAI, self).__init__(*args, **kwargs)

    def score(self, state, ai_move, depth):
        if self._game.is_game_over(state):
            return super(HeuristicAI, self).score(state, depth)
        try:
            return self._score_cache[(state, ai_move)]
        except KeyError:
            pass

        if ai_move:
            piece_move = self._game.ai_piece
        else:
            piece_move = self._game.player_piece
        win_count = self._game.win_count
        scores = {
            self._game.ai_piece: 0,
            self._game.player_piece: 0
        }
        for line in self._game.possible_winning_lines(state):
            line = shrink(line)
            for i, (piece, count) in enumerate(line):
                if piece != self._game.empty_place:
                    prev = line[i-1] if i > 0 else None
                    next = line[i+1] if i+1 < len(line) else None
                    mult = 0
                    total_empty = 0
                    if prev and prev[0] == self._game.empty_place:
                        total_empty += prev[1]
                        mult += 1
                    if next and next[0] == self._game.empty_place:
                        total_empty += next[1]
                        mult += 1
                    if ((mult > 0 and count == win_count - 1 and
                        piece_move == piece) or
                       (mult > 1 and count == win_count-1) or
                       (mult > 1 and count == win_count-2 and
                       piece_move == piece and total_empty > 2)):
                        mult += 1000

                    if total_empty + count < win_count:
                        mult = 0

                    scores[piece] += count * mult
        score = scores[self._game.ai_piece] -\
            scores[self._game.player_piece]
        self._score_cache[(state, ai_move)] = score
        return score

    def minimax(self, state, is_max, depth):
        if self._game.is_game_over(state) or depth >= self.max_depth:
            return (self.score(state, is_max, depth), (-1, -1))
        return super(HeuristicAI, self).minimax(state, is_max, depth)
