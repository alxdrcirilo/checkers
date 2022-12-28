import logging
from random import choice

from checkers.board import Board
from checkers.nodes import Node
from checkers.piece import Piece, Player

logging.basicConfig(level=logging.INFO)


class NoMoves(Exception):
    def __init__(self, player: Player) -> None:
        self.player = player
        self.message = f"{player} ran out of moves"
        super().__init__(self.message)


class NoPieces(Exception):
    def __init__(self, player: Player) -> None:
        self.player = player
        self.message = f"{player} ran out of pieces"
        super().__init__(self.message)


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

    def random_move(self) -> None:
        """
        Make a random move.
        """
        nodes = self.board._get_player_nodes(self.player)

        # Get random move
        try:
            # Enforce jump moves
            if nodes["jump"]:
                logging.info("type: jump")
                pos, root = choice(list(nodes["jump"].items()))
                jump = True

            # Otherwise get regular moves
            else:
                logging.info("type: free")
                pos, root = choice(list(nodes["free"].items()))
                jump = False

            piece = self.board.pieces[pos]
            self._traverse(piece, root, jump)

        except IndexError:
            if list(self.board._get_player_pos(self.player)):
                raise NoMoves(self.player)
            else:
                raise NoPieces(self.player)

    # TODO: add docstring
    def _traverse(self, piece: Piece, node: Node, capture: bool = False) -> None:
        # Force jumps
        if capture:
            jumps = [x for x in node.children if x.captured]

            if jumps:
                # Get random child
                child = choice(jumps)

                # Capture node
                captured = self.board.state[child.captured]

                # Move piece
                self.board.move(piece, node.position, child.position)

                logging.info(f"mov: {piece.symbol} {node.position} 🡒 {child.position}")
                logging.info(f"del: {captured.symbol} {child.captured}")

                # Remove captured piece
                self.board._remove(child.captured)

                piece = self.board.state[child.position]
                self._traverse(piece, child, True)

                # yield (child.position, child.captured)
                # yield from self._traverse(child, True)

        # Free squares
        else:
            child = choice(node.children)
            self.board.move(piece, node.position, child.position)
            logging.info(f"mov: {piece.symbol} {node.position} 🡒 {child.position}")

            # yield child.position

    # TODO: add docstring
    def play(self) -> None:
        while not self.winner:
            logging.info(f"player: {self.player}")

            try:
                self.random_move()

            except NoMoves as exception:
                print(exception)
                self.next_turn()
                self.winner = self.player
                break

            except NoPieces as exception:
                print(exception)
                self.next_turn()
                self.winner = self.player
                break

            self.next_turn()
            print(self.board)
