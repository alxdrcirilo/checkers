from checkers.board import Board
from checkers.piece import Player


class Game:
    """
    Game class.

    Represents the game.
    Contains methods required to play.
    Contains useful properties to the game.
    """

    def __init__(self) -> None:
        """
        Initialize board, player, and winner.
        Player 'BLACK' starts.
        """
        self._board = Board()
        self._player = Player.BLACK
        self._winner = None

    @property
    def board(self) -> Board:
        """
        Return <board> property.

        :return Board: board
        """
        return self._board

    @property
    def player(self) -> Player:
        """
        Return <player> property.

        :return Player: player
        """
        return self._player

    @player.setter
    def player(self, player: Player) -> None:
        """
        Set <player> property.

        :param Player player: player
        """
        self._player = player

    @property
    def players(self) -> set:
        """
        Return the players currently in game.

        :return set: players in game
        """
        return set(x.player for x in self.board.pieces.values())

    @property
    def winner(self) -> Player | None:
        """
        Return <winner> property.

        :return Player | None: winner or None
        """
        return self._winner

    @winner.setter
    def winner(self, player: Player) -> None:
        """
        Set <winner> property.

        :param Player player: player
        """
        self._winner = player

    def next_turn(self) -> None:
        """
        Set the next player.
        """
        self.player = Player.__call__(-self.player.value)
