import pytest

from checkers.logic.board import Board
from checkers.logic.piece import Piece, Player, Rank


@pytest.fixture
def board() -> Board:
    return Board()


class TestBoard:
    def test_str(self, board: Board):
        assert isinstance(board.__str__(), str)

    def test_state(self, board: Board):
        assert len(board.state) == 64
        assert isinstance(board.state, dict)
        board.state = ((2, 0), Piece(Player.BLACK, Rank.PAWN))
        assert board._state[(2, 0)] == Piece(Player.BLACK, Rank.PAWN)
