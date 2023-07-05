from checkers.logic.board import Board
from checkers.logic.piece import Player


class NoMoves(Exception):
    def __init__(self, player: Player) -> None:
        super().__init__(f"{player} ran out of moves")


class Game:
    """
    Game class.

    Represents the game.
    Contains methods required to play.
    Contains useful properties to the game.
    """

    def __init__(self) -> None:
        """
        Initialize board, player, winner, and turn.
        Player 'BLACK' starts.
        """
        self._board = Board()
        self._player = Player.BLACK
        self._winner = None
        self._turn = 0

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

    @property
    def stats(self) -> str:
        """
        Returns some game statistics.

        :return str: statistics
        """
        return f"{self.winner=}\n{self._turn=}"

    def next_turn(self) -> None:
        """
        Set the next player.
        """
        self.player = Player(-self.player.value)
        self._turn += 1
