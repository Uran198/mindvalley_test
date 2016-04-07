from .exceptions import IllegalMoveError, ImpossibleGameError


class Game:
    """
    Makes sure the moves are made are legal.
    Interacts with AI and gives interface to interact with player.

    Assumes that player is playing with 'x' and ai - 'o'
    """

    def __init__(self, lines, columns):
        if lines <= 0 or columns <= 0:
            raise ImpossibleGameError
        self._player_piece = "x"
        self._ai_piece = "o"
        self._state = []
        for _ in range(lines):
            line = []
            for _ in range(columns):
                line.append(".")
            self._state.append(line)

    def make_move(self, line, column):
        line -= 1
        column -= 1
        if not (0 < line < len(self._state) and
                0 < column < len(self._state[0])):
            raise IllegalMoveError("Value is outside of the box.")
        if self._state[line][column] != ".":
            raise IllegalMoveError("Place is already taken.")

        self._state[line][column] = self._player_piece

    @property
    def state(self):
        return [''.join(line) for line in self._state]
