import logging
from random import choice

from checkers.ai.ab_pruning import AlphaBetaPruning
from checkers.exceptions.moves import NoMoves
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

    def get_ai_move(self, player: Player, depth: int) -> list:
        """
        Return the best move by a given player using alpha-beta pruning AI.

        :param Player player: player
        :param int depth: depth of alpha-beta pruning search
        """
        ai = AlphaBetaPruning()
        best_move, _ = ai.minimax(
            game=self,
            depth=depth,
            maximizer=True,
            max_player=player,
        )
        return best_move

    def _make_move(self, path: list) -> None:
        """
        Make opponent moves based on path.

        :param list path: move
        """
        while len(path) > 1:
            source, _ = path.pop(0)
            target, capture = path[0]

            # Move
            piece = self.board.pieces[source]
            self.board.move(piece=piece, old=source, new=target)
            logging.info(f"{piece} MOVED from {source} to {target}")

            # Cature
            if capture:
                captured_piece = self.board.pieces[capture]
                self.board.remove(pos=capture)
                logging.info(f"{captured_piece} CAPTURED at {capture}")

    def is_game_over(self) -> bool:
        """
        Returns True if the game is over.

        :raises NoMoves: when a given player runs out of moves
        :return bool: True if game is over, False otherwise
        """
        try:
            for player in [Player.BLACK, Player.WHITE]:
                if not self.board.get_player_moves(player):
                    self.winner = Player(-self.player.value)
                    raise NoMoves(player)
        except NoMoves:
            return True
        return False
