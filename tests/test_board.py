from collections.abc import Generator

import pytest

from checkers.logic.board import Board
from checkers.logic.piece import Piece, Player, Rank


@pytest.fixture
def board() -> Board:
    return Board()


class TestBoard:
    def test_str(self, board: Board) -> None:
        assert isinstance(board.__str__(), str)

    def test_state(self, board: Board) -> None:
        assert len(board.state) == 64
        assert isinstance(board.state, dict)
        board.state = ((2, 0), Piece(Player.BLACK, Rank.PAWN))
        assert board._state[(2, 0)] == Piece(Player.BLACK, Rank.PAWN)

    @pytest.mark.parametrize(
        "piece, position, rank",
        [
            (Piece(player=Player.WHITE, rank=Rank.PAWN), (7, 0), Rank.KING),
            (Piece(player=Player.WHITE, rank=Rank.PAWN), (5, 2), Rank.PAWN),
            (Piece(player=Player.BLACK, rank=Rank.PAWN), (0, 1), Rank.KING),
            (Piece(player=Player.BLACK, rank=Rank.PAWN), (2, 7), Rank.PAWN),
        ],
    )
    def test_is_king(
        self, board: Board, piece: Piece, position: tuple[int, int], rank: Rank
    ) -> None:
        board._is_king(piece, position)
        assert piece.rank is rank

    @pytest.fixture(scope="function")
    @pytest.mark.parametrize("position", [(0, 1), (2, 1)])
    def test_remove(self, board: Board, position: tuple[int, int]) -> None:
        # Assert that piece to be removed is a 'Piece'
        removed_piece = board._state[position]
        assert isinstance(removed_piece, Piece)

        # Remove piece
        captured = board._remove(position)

        # Assert piece has been removed
        assert not board._state[position]
        assert isinstance(captured, Piece)
        assert captured is removed_piece

    @pytest.mark.usefixtures("test_remove")
    @pytest.mark.parametrize(
        "position, piece",
        [
            ((0, 1), Piece(player=Player.WHITE, rank=Rank.PAWN)),
            ((2, 1), Piece(player=Player.WHITE, rank=Rank.PAWN)),
        ],
    )
    def test_restore(
        self, board: Board, position: tuple[int, int], piece: Piece
    ) -> None:
        # Assert no piece at given position
        assert not board._state[position]

        # Restore piece
        board._restore(position, piece)

        # Assert piece has been restored
        assert board._state[position] is piece

    @pytest.mark.parametrize(
        "expected",
        [
            [
                (5, 0),
                (5, 2),
                (5, 4),
                (5, 6),
                (6, 1),
                (6, 3),
                (6, 5),
                (6, 7),
                (7, 0),
                (7, 2),
                (7, 4),
                (7, 6),
            ]
        ],
    )
    def test_get_player_pos(self, board: Board, expected: Generator) -> None:
        assert list(board._get_player_pos(player=Player.BLACK)) == expected

    @pytest.mark.parametrize(
        "expected",
        [
            [
                (5, 0),
                (5, 2),
                (5, 4),
                (5, 6),
            ]
        ],
    )
    def test_get_player_moves(self, board: Board, expected: Generator) -> None:
        assert list(board._get_all_player_moves(player=Player.BLACK)) == expected

    @pytest.mark.skip("WIP`")
    def test_get_piece_moves(self, board: Board) -> None:
        pass

    @pytest.mark.parametrize(
        "piece, old, new",
        [
            (Piece(Player.WHITE, Rank.PAWN), (2, 1), (3, 0)),
            (Piece(Player.BLACK, Rank.PAWN), (5, 6), (4, 5)),
        ],
    )
    def test_move(
        self, board: Board, piece: Piece, old: tuple[int, int], new: tuple[int, int]
    ) -> None:
        assert not board._state[new]
        board.move(piece, old, new)
        assert board._state[new] is piece
