import pytest

from checkers.logic.board import Board
from checkers.logic.game import Game, NoMoves
from checkers.logic.piece import Player


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
        assert game.stats == "self.winner=None\nself._turn=0"

    @pytest.mark.parametrize("player", [Player.BLACK, Player.WHITE])
    def test_no_moves_exception(self, player: Player) -> None:
        with pytest.raises(NoMoves) as exc_info:
            raise NoMoves(player)

        assert str(exc_info.value) == f"{player} ran out of moves"
