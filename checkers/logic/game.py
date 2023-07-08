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

    def is_game_over(self) -> bool:
        """
        Check if the game is over (i.e. opponent has no more moves).
        Sets winner accordingly.

        :return bool: True if game is over
        """
        for player in [Player.BLACK, Player.WHITE]:
            try:
                opponent = Player(-player.value)
                if not self.board._get_all_player_moves(player=opponent):
                    raise NoMoves(opponent)
                return False

            except NoMoves:
                self.winner = player
                return True

        return False
