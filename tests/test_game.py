import pytest

from checkers.board import Board
from checkers.game import Game
from checkers.piece import Player


@pytest.fixture
def game() -> Game:
    return Game()


class TestGame:
    def test_board(self, game: Game):
        assert type(game.board) is Board

    def test_player(self, game: Game):
        assert game.player is Player.BLACK
        game.next_turn()
        assert game.player is Player.WHITE

    def test_players(self, game: Game):
        assert game.players == set([Player.BLACK, Player.WHITE])

    def test_winner(self, game: Game):
        assert game.winner is None
        game.winner = Player.BLACK
        assert game.winner is Player.BLACK
