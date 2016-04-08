

class IllegalMoveError(ValueError):
    """
    Raised when an attempt to make an illegal move was made.
    """
    pass


class ImpossibleGameError(ValueError):
    """
    Raised when as attempt is made to create an impossible game.
    For example without less than 0 number of rows or columns.
    """
    pass


class InvalidAIError(ValueError):
    """
    Raised when an AI tries to make illegal move.
    """
    pass
