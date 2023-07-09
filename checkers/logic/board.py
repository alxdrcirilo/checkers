import numpy as np

from checkers.exceptions.moves import NoMoves
from checkers.logic.node import Node
from checkers.logic.piece import Piece, Player, Rank


class Board:
    """
    Board class.

    Represents the board.
    Contains methods required to interact with the board.
    Contains useful properties of the board.
    """

    Cell = tuple[int, int]

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
                    state[(x, y)] = Piece(Player.WHITE, Rank.PAWN)  # type: ignore
                elif x > 4:
                    state[(x, y)] = Piece(Player.BLACK, Rank.PAWN)  # type: ignore

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
    def state(self, data: tuple[Cell, Piece | int]) -> None:
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

    def _is_king(self, piece: Piece, pos: Cell) -> None:
        """
        Converts a piece's rank to 'KING' if applicable.

        :param Piece piece: piece
        "param Cell pos: position
        """
        if piece.rank is Rank.PAWN:
            x, _ = pos
            if piece.player is Player.BLACK and x == 0:
                piece.rank = Rank.KING

            elif piece.player is Player.WHITE and x == 7:
                piece.rank = Rank.KING

    def remove(self, pos: Cell) -> Piece:
        """
        Remove piece at a given (<x>, <y>) position.

        :param Cell pos: position
        """
        captured = self.pieces[pos]
        self._state[pos] = None
        return captured

    def restore(self, pos: Cell, piece: Piece) -> None:
        """
        Restore piece at a given (<x>, <y>) position.

        :param Cell pos: position
        :param Piece piece: captured piece
        """
        self._state[pos] = piece

    def _get_pieces(self, player: Player) -> list:
        """
        Return player's pieces positions.

        :param Player player: player
        :return list: list of pieces positions for a given player
        """
        return [pos for pos, piece in self.pieces.items() if piece.player is player]

    def get_player_moves(self, player: Player) -> list:
        """
        Return the positions of the pieces that a given player can move.
        Captures are compulsory. If no capture is available, return regular moves.

        :param Player player: player
        :return list: pieces positions that a given player can move
        """
        captures = self._get_player_captures(player)
        if not captures:
            return list(self._get_player_tree(player).keys())
        return captures

    def _get_player_captures(self, player: Player) -> list:
        """
        Return the positions of the pieces that can capture other pieces for a given player.

        :param Player player: player
        :return list: pieces positions for a given player than can capture opponent pieces
        """

        def _get_captures(moves: list) -> list:
            """
            Return the captured positions if any.

            :param list moves: list of moves
            :return list: list of capture positions
            """
            return [
                move[1][1] if isinstance(move[1], tuple) else None for move in moves
            ]

        moves = self._get_player_tree(player)
        captures = {pos: set(_get_captures(moves)) for pos, moves in moves.items()}
        return list(filter(lambda pos: any(captures[pos]), captures))

    def _get_player_tree(self, player: Player) -> dict:
        """
        Return the player's nodes based on its available pieces.
        Kings have special move attributes depending on the board configuration.
        Position is optional, if given: returns the moves at given position.

        :param Player player: player
        :return dict: dict {<type>: {<position>: <node>}}
        """
        moves = {}
        for pos in self._get_pieces(player):
            root = Node(pos)
            node = self._get_piece_tree(root)

            # Only get pieces that can move
            if node.children:
                paths = node._get_paths()
                moves[node.position] = paths

        return moves

    def _get_piece_tree(
        self,
        node: Node,
        directions: list = [],
        from_capture: bool | None = None,
    ) -> Node:
        """
        Return the moves (tree) a piece can make.

        :param Node node: node (tree)
        :param list directions: directions a piece can take
        :param bool | None from_capture: if parent node captured, don't add child if free cell
        :return Node: node (tree) of moves
        """

        def _is_allowed(pos) -> bool:
            """
            Return whether a move can be made (i.e. in 8x8 board).

            :param Cell pos: position
            :return bool: 'True' if move is allowed
            """
            x, y = pos
            return x in range(8) and y in range(8)

        def _is_free(pos) -> bool:
            """
            Return whether a Cell is free.

            :param Cell pos: position
            :return bool: 'True' if node is free
            """
            return not self._state[pos]

        def _is_capture(pos) -> bool:
            """
            Return whether a piece can be captured.

            :param Cell pos: position
            :return bool: 'True' if piece can be captured
            """
            return _is_allowed(pos) and _is_free(pos)

        def _is_opponent(pos) -> bool:
            """
            Return whether it is the opponent piece.

            :param Cell pos: position
            :return bool: 'True' if it is the opponent piece
            """
            opponent = self._state[pos].player.value
            return player != opponent

        pos = node.position
        piece = self.pieces[pos]
        player = piece.player.value

        # Override directions
        if not directions:
            directions = piece.directions

        # Pick a direction from current position
        for dir in directions:
            a, b = dir
            x, y = pos
            move = tuple((x + a, y + b))

            # Only check allowed moves
            if _is_allowed(move):
                # Busy cell
                if self._state[move]:
                    # Check if capture is possible
                    if _is_opponent(move):
                        x, y = move
                        next_pos = tuple((x + a, y + b))

                        if _is_capture(next_pos):
                            self.move(piece, pos, next_pos)

                            child = Node(position=next_pos)
                            child.captured = move
                            captured = self.remove(move)
                            node.children.append(child)

                            if piece.rank is Rank.KING:
                                dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                                dirs.remove((-a, -b))
                            else:
                                dirs = []

                            self._get_piece_tree(
                                node=child, directions=dirs, from_capture=True
                            )

                            # Undo move
                            self.move(piece, next_pos, pos)

                            # Restore captured piece
                            self.restore(pos=move, piece=captured)

                # Free cell
                # Skip if coming from previous capture
                elif not from_capture:
                    child = Node(position=move)
                    node.children.append(child)

        return node

    def move(self, piece: Piece, old: Cell, new: Cell) -> None:
        """
        Move a piece from <old> to <new> position:
            - Set <old> position to unoccupied (i.e. 0).
            - Set <new> position for <piece>.

        Check if piece can be converted to 'KING'.

        :param Piece piece: piece
        :param Cell old: old position
        :param Cell new: new position
        """
        self.state = (old, 0)
        self.state = (new, piece)

        self._is_king(piece, new)

    def is_game_over(self) -> bool:
        """
        Returns True if the game is over.

        :raises NoMoves: when a given player runs out of moves
        :return bool: True if game is over, False otherwise
        """
        try:
            for player in [Player.BLACK, Player.WHITE]:
                if not self.get_player_moves(player):
                    raise NoMoves(player)
        except NoMoves:
            return True
        return False
