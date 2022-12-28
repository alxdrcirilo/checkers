from collections.abc import Generator

import numpy as np

from checkers.nodes import Node
from checkers.piece import Piece, Player, Rank


class Board:
    """
    Board class.

    Represents the board.
    Contains methods required to interact with the board.
    Contains useful properties of the board.
    """

    Square = tuple[int, int]

    def __init__(self) -> None:
        """
        Initialize the state of the board.
        """
        self._state = self._get_state()

    def _get_state(self) -> dict:
        """
        Return the initial state of the board.

        :return dict: state
        """
        state = {(x, y): None for x in range(8) for y in range(8)}
        for x, y in state:
            if (x + 1) % 2 == y % 2:
                if x < 3:
                    state[(x, y)] = Piece(Player.WHITE, Rank.PAWN)
                elif x > 4:
                    state[(x, y)] = Piece(Player.BLACK, Rank.PAWN)

        return state

    def __str__(self) -> str:
        """
        Return a string representation of the board.

        :return str: board
        """
        board = np.zeros(shape=(8, 8), dtype=np.int8)
        for pos, piece in self.pieces.items():
            board[pos] = piece.__hash__()

        return str(board)

    @property
    def state(self) -> dict:
        """
        Return <state> property.

        :return dict: state
        """
        return self._state

    @state.setter
    def state(self, data: tuple[Square, Piece | int]) -> None:
        """
        Set <state> property.

        :param tuple data: (<x, y>, <Piece>)
        """
        pos, piece = data
        self._state[pos] = piece

    @property
    def pieces(self) -> dict:
        """
        Return all the pieces currently in game.

        :return dict: pieces in game {<position>: <Piece>}
        """
        return {k: v for k, v in self._state.items() if type(v) is Piece}

    def _remove(self, pos: Square) -> None:
        """
        Remove piece at a given (<x>, <y>) position.

        :param Square pos: position
        """
        self._state[pos] = None

    def _get_player_pos(self, player: Player) -> Generator:
        """
        Return player's pieces positions.

        :param Player player: player
        :return list: Generator of pieces positions for a given player
        """
        for pos, piece in self.pieces.items():
            if piece.player is player:
                yield (pos)

    def _get_player_nodes(self, player: Player) -> dict:
        """
        Return the player's nodes based on its available pieces.

        :param Player player: player
        :return dict: dict {<type>: {<position>: <node>}}
        """
        nodes = {"jump": dict(), "free": dict()}

        for pos in self._get_player_pos(player):
            root = Node(pos)
            node = self.get_moves(pos, root)

            # Only get pieces that can move
            if node.children:
                if any([child.captured for child in node.children]):
                    nodes["jump"][node.position] = node
                else:
                    nodes["free"][node.position] = node

        return nodes

    def get_moves(self, pos: Square, node: Node) -> Node:
        """
        Return the moves (tree) a piece can make.

        :param Square pos: position
        :param Node node: node (tree)
        :return Node: node (tree) of moves
        """

        def _is_allowed(pos) -> bool:
            """
            Return whether a move can be made (i.e. in 8x8 board).

            :param Square pos: position
            :return bool: 'True' if move is allowed
            """
            x, y = pos
            return x in range(8) and y in range(8)

        def _is_capture(pos) -> bool:
            """
            Return whether a piece can be captured.

            :param Square pos: position
            :return bool: 'True' if piece can be captured
            """
            return _is_allowed(pos) and _is_free(pos)

        def _is_free(pos) -> bool:
            """
            Return whether a square is free.

            :param Square pos: position
            :return bool: 'True' if node is free
            """
            return not self._state[pos]

        def _is_opponent(pos) -> bool:
            """
            Return whether it is the opponent piece.

            :param Square pos: position
            :return bool: 'True' if it is the opponent piece
            """
            opponent = self._state[pos].player.value
            return player != opponent

        piece = self.pieces[pos]
        player = piece.player.value

        for dir in piece.allowed_moves:
            x, y = pos
            a, b = dir
            move = tuple((x + a, y + b))

            # Only check allowed moves
            if _is_allowed(move):

                # Busy
                if self._state[move]:

                    # Check if capture is possible
                    if _is_opponent(move):
                        x, y = move
                        next_pos = tuple((x + a, y + b))

                        if _is_capture(next_pos):
                            self.move(piece, pos, next_pos)

                            child = Node(position=next_pos)
                            child.captured = move
                            node.children.append(child)

                            self.get_moves(next_pos, child)

                            # Undo move
                            self.move(piece, next_pos, pos)

                # Free
                else:
                    child = Node(position=move)
                    node.children.append(child)

        return node

    def move(self, piece: Piece, old: Square, new: Square) -> None:
        """
        Move a piece from <old> to <new> position.

        :param Piece piece: piece
        :param Square old: old position
        :param Square new: new position
        """
        self.state = (old, 0)
        self.state = (new, piece)
