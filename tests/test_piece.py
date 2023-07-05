import pytest

from checkers.logic.piece import Piece, Player, Rank


# TODO: add piece fixture that can be shared by all tests
class TestPiece:
    @pytest.mark.parametrize(
        "piece, hash",
        [
            (Piece(Player.BLACK, Rank.PAWN), -1),
            (Piece(Player.BLACK, Rank.KING), -2),
            (Piece(Player.WHITE, Rank.PAWN), 1),
            (Piece(Player.WHITE, Rank.KING), 2),
        ],
    )
    def test_hash(self, piece: Piece, hash: int) -> None:
        assert piece.__hash__() == hash

    @pytest.mark.parametrize(
        "piece, symbol",
        [
            (Piece(Player.BLACK, Rank.PAWN), "⛀"),
            (Piece(Player.BLACK, Rank.KING), "⛁"),
            (Piece(Player.WHITE, Rank.PAWN), "⛂"),
            (Piece(Player.WHITE, Rank.KING), "⛃"),
        ],
    )
    def test_symbol(self, piece: Piece, symbol: str) -> None:
        assert piece.symbol == symbol
