from random import choice

from checkers.logic.board import Board
from checkers.logic.piece import Player


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
        self._turn = 1

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

    @property
    def turn(self) -> int:
        """
        Return the turn number (e.g. 24).

        :return int: turn
        """
        return self._turn

    def next_turn(self, multiple_jump: bool = False) -> None:
        """
        Set the next player.

        :param bool multiple_jump: True if player is doing multiple jump
        """
        if not multiple_jump:
            self.player = Player(-self.player.value)
        self._turn += 1

    def get_random_move(self, player: Player) -> list:
        """
        Return a random move by a given player.

        :param Player player: player
        :return Cell: position of random move
        """
        random_piece = choice(self.board.get_player_moves(player))
        random_move = choice(self.board._get_player_tree(player)[random_piece])
        return random_move
