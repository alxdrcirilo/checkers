from checkers.logic.game import Game
from checkers.logic.piece import Rank


class MockGame(Game):
    def __init__(self) -> None:
        super().__init__()
        self.config_board()

    def config_board(self):
        """
        Setup the board for development purposes (e.g. debugging).

        :param Game game: current game state
        """
        # Move a few pieces
        pieces_to_move = [
            [(0, 7), (2, 5)],
            [(1, 0), (2, 1)],
            [(2, 7), (4, 5)],
            [(5, 0), (3, 2)],
        ]
        for old, new in pieces_to_move:
            self.board.move(self.board.pieces[old], old, new)

        # Remove a few pieces
        pieces_to_remove = [
            (1, 2),
            (1, 4),
            (1, 6),
            (5, 4),
            (6, 1),
            (6, 5),
            (7, 4),
        ]
        for piece in pieces_to_remove:
            self.board._remove(piece)

        # Convert a few pawns to kings
        pieces_to_crown = [(2, 5), (3, 2), (5, 6)]
        for piece in pieces_to_crown:
            piece = self.board.pieces[piece]
            piece.rank = Rank.KING
