import numpy as np

from checkers.piece import Piece, Player, Rank


class Board:
    """
    Board class.

    Represents the board.
    Contains methods required to interact with the board.
    Contains useful properties of the board.
    """

    def __init__(self) -> None:
        """
        Initialize the state of the board.
        """
        self._state = self._get_state()

    def _get_state(self) -> dict:
        """
        Return the initial state of the board.

        :return dict: state
        """
        state = {(x, y): 0 for x in range(8) for y in range(8)}
        for x, y in state:
            if (x + 1) % 2 == y % 2:
                if x < 3:
                    state[(x, y)] = Piece(Player.WHITE, Rank.PAWN)
                elif x > 4:
                    state[(x, y)] = Piece(Player.BLACK, Rank.PAWN)

        return state

    def __str__(self) -> str:
        """
        Return a string representation of the board.

        :return str: board
        """
        board = np.zeros(shape=(8, 8), dtype=np.int8)
        for pos, piece in self.pieces.items():
            board[pos] = piece.__hash__()

        return str(board)

    @property
    def state(self) -> dict:
        """
        Return <state> property.

        :return dict: state
        """
        return self._state

    @state.setter
    def state(self, data: tuple[tuple[int, int], Piece]) -> None:
        """
        Set <state> property.

        :param tuple data: (<x, y>, <Piece>)
        """
        pos, piece = data
        self._state[pos] = piece

    @property
    def pieces(self) -> dict:
        """
        Return all the pieces currently in game.

        :return dict: pieces in game {<position>: <Piece>}
        """
        return {k: v for k, v in self._state.items() if type(v) is Piece}
