from collections import defaultdict

from .ai import get_default_ai
from .exceptions import IllegalMoveError, ImpossibleGameError, InvalidAIError


class Game:
    """
    Makes sure the moves are made are legal.
    Interacts with AI and gives interface to interact with player.

    Assumes that player is playing with 'x' and ai - 'o'
    """

    def __init__(self, lines, columns, win_count=3):
        if lines <= 0 or columns <= 0:
            raise ImpossibleGameError
        self._player_piece = "x"
        self._ai_piece = "o"
        self._ai = None
        self._win_count = win_count
        self._state = []
        for _ in range(lines):
            line = []
            for _ in range(columns):
                line.append(".")
            self._state.append(line)

    def _ai_make_move(self):
        line, column = self._ai.next_move()
        if not (0 <= line < len(self._state) and
                0 <= column < len(self._state[0])):
            raise InvalidAIError("AI tried to make a move outside the board.")
        if self._state[line][column] != '.':
            msg = "AI tried to place piece in already occupied place."
            raise InvalidAIError(msg)

        self._state[line][column] = self._ai_piece

    def start(self, ai_class=None, player_first=False):
        for i, row in enumerate(self._state):
            for j, _ in enumerate(row):
                self._state[i][j] = '.'

        if ai_class:
            self._ai = ai_class(self, self._ai_piece)
        else:
            self._ai = get_default_ai(self, self._ai_piece)

        if not player_first:
            self._ai_make_move()

    def make_move(self, line, column):
        """
        Makes move on behalf of the player on the specified line and column.
        Throws IllegalMoveError when place is already taken or the move is
        outside of the board.
        """
        line -= 1
        column -= 1
        if not (0 <= line < len(self._state) and
                0 <= column < len(self._state[0])):
            raise IllegalMoveError("Value is outside of the box.")
        if self._state[line][column] != ".":
            raise IllegalMoveError("Place is already taken.")

        self._state[line][column] = self._player_piece
        self._ai_make_move()

    @property
    def state(self):
        return [''.join(line) for line in self._state]

    def get_winner(self):
        """
        Returns the winner based on the game state.
        If the game state contains several winners, function may return any
        value.
        """
        def winner_from_line(line):
            if line.count(self._ai_piece) >= self._win_count:
                return "ai"
            if line.count(self._player_piece) >= self._win_count:
                return "player"
            return None

        for line in self._state:
            winner = winner_from_line(''.join(line))
            if winner:
                return winner

        cols = defaultdict(lambda: [])
        for line in self._state:
            for i, col in enumerate(line):
                cols[i] += col
        for line in cols.values():
            winner = winner_from_line(''.join(line))
            if winner:
                return winner

        # Going through diagonals
        columns = len(self._state[0])
        for offset in range(-columns, columns):
            main = [row[i+offset]
                    for i, row in enumerate(self._state)
                    if 0 <= i+offset < columns
                    ]
            counter = [row[-i+offset]
                       for i, row in enumerate(self._state)
                       if 0 <= -i+offset < columns
                       ]
            winner = winner_from_line(''.join(main))
            if not winner:
                winner = winner_from_line(''.join(counter))
            if winner:
                return winner

        return None
