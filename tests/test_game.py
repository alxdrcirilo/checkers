import pytest

from checkers.exceptions.moves import NoMoves
from checkers.logic.board import Board
from checkers.logic.game import Game
from checkers.logic.piece import Piece, Player


@pytest.fixture
def game() -> Game:
    return Game()


class TestGame:
    def test_board(self, game: Game) -> None:
        assert type(game.board) is Board

    def test_player(self, game: Game) -> None:
        assert game.player is Player.BLACK
        game.next_turn()
        assert game.player is Player.WHITE

    def test_players(self, game: Game) -> None:
        assert game.players == set([Player.BLACK, Player.WHITE])

    def test_winner(self, game: Game) -> None:
        assert game.winner is None
        game.winner = Player.BLACK
        assert game.winner is Player.BLACK

    def test_stats(self, game: Game) -> None:
        assert game.stats == "self.winner=None\nself._turn=1"

    def test_turn(self, game: Game) -> None:
        assert game.turn is 1

    @pytest.mark.parametrize("player", [Player.BLACK, Player.WHITE])
    def test_no_moves_exception(self, player: Player) -> None:
        with pytest.raises(NoMoves) as exc_info:
            raise NoMoves(player)

        assert str(exc_info.value) == f"{player} ran out of moves"

    def test_random_move(self, game: Game) -> None:
        move = game.get_random_move(player=Player.BLACK)
        assert type(move) is list and len(move[0]) == 2

    def test_ai_move(self, game: Game) -> None:
        move = game.get_ai_move(player=Player.BLACK, depth=1)
        assert type(move) is list and len(move[0]) == 2

    def test_game_over(self, game: Game) -> None:
        # Game is not over
        assert game.is_game_over() is False

        # Remove all WHITE pieces
        for position, piece in game.board.state.items():
            if type(piece) is Piece:
                if piece.player is Player.WHITE:
                    game.board.remove(position)

        # Game is over
        assert game.is_game_over() is True
