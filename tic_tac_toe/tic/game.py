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
                line.append(self.empty_place)
            self._state.append(line)

    @staticmethod
    def get_next_state(state, line, column, piece):
        """
        Returns new state based on the move.
        Makes no checks if the move is legal.
        """
        next_state = []
        for i, row in enumerate(state):
            new_row = ''
            for j, val in enumerate(row):
                if i == line and j == column:
                    new_row += piece
                else:
                    new_row += val
            next_state.append(new_row)
        return next_state

    def _ai_make_move(self):
        line, column = self._ai.next_move()
        if not (0 <= line < len(self._state) and
                0 <= column < len(self._state[0])):
            raise InvalidAIError("AI tried to make a move outside the board.")
        if self._state[line][column] != self.empty_place:
            msg = "AI tried to place piece in already occupied place."
            raise InvalidAIError(msg)

        self._state[line][column] = self._ai_piece

    def start(self, ai_class=None, player_first=False):
        for i, row in enumerate(self._state):
            for j, _ in enumerate(row):
                self._state[i][j] = self.empty_place

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
        if self.is_game_over():
            raise IllegalMoveError("Can't make move in end of game position.")
        line -= 1
        column -= 1
        if not (0 <= line < len(self._state) and
                0 <= column < len(self._state[0])):
            raise IllegalMoveError("Value is outside of the box.")
        if self._state[line][column] != self.empty_place:
            raise IllegalMoveError("Place is already taken.")

        self._state[line][column] = self._player_piece

        if not self.is_game_over():
            self._ai_make_move()

    @property
    def state(self):
        return [''.join(line) for line in self._state]

    @property
    def empty_place(self):
        return '.'

    @property
    def ai_piece(self):
        return self._ai_piece

    @property
    def player_piece(self):
        return self._player_piece

    def is_game_over(self, state=None):
        if state is None:
            state = self.state
        return (self.get_winner(state) is not None or
                ''.join(state).count(self.empty_place) == 0)

    def get_winner(self, state=None):
        """
        Returns the winner based on the game state.
        If the game state contains several winners, function may return any
        value.
        """
        if state is None:
            state = self.state

        def winner_from_line(line):
            if line.count(self._ai_piece) >= self._win_count:
                return "ai"
            if line.count(self._player_piece) >= self._win_count:
                return "player"
            return None

        for line in state:
            winner = winner_from_line(''.join(line))
            if winner:
                return winner

        cols = defaultdict(lambda: [])
        for line in state:
            for i, col in enumerate(line):
                cols[i] += col
        for line in cols.values():
            winner = winner_from_line(''.join(line))
            if winner:
                return winner

        # Going through diagonals
        columns = len(state[0])
        for offset in range(-columns, columns):
            main = [row[i+offset]
                    for i, row in enumerate(state)
                    if 0 <= i+offset < columns
                    ]
            counter = [row[-i+offset]
                       for i, row in enumerate(state)
                       if 0 <= -i+offset < columns
                       ]
            winner = winner_from_line(''.join(main))
            if not winner:
                winner = winner_from_line(''.join(counter))
            if winner:
                return winner

        return None
