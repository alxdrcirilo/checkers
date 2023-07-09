import sys

import pygame

from checkers.graphics.sprites.piece import PieceSprite
from checkers.graphics.window import Window
from checkers.logic.piece import Player
from checkers.utils.logging import logging


class Environment(Window):
    """
    Environment class.

    Represents the game environment.
    """

    def __init__(self) -> None:
        """
        Initialize the environment.

        :ivar PLAYER_MOVES: list of pieces (positions) that the current player can move
        :ivar HUMAN_PLAYER: human player (BLACK piece)
        :ivar MULTIPLE_CAPTURE: (x, y) pixel coordinates of piece position if in multiple capture path
        :ivar SELECTED: currently selected game piece
        """
        super().__init__()

        # Initialize instance variables
        self.PLAYER_MOVES: list = self.board.get_player_moves(self.player)
        self.HUMAN_PLAYER: Player = Player.BLACK
        self.MULTIPLE_CAPTURE: tuple | None = None
        self.SELECTED: PieceSprite | None = None

        # Set human player as starting player
        self.player = self.HUMAN_PLAYER
        logging.info(f"Started game with {self.player}")

    def __stop_multiple_capture(self):
        """
        Helper method to stop multiple capture.
        """
        self.next_turn()
        logging.info(f"Next turn: {self.turn} player: {self.player}")

        self.PLAYER_MOVES = self.board.get_player_moves(self.player)
        self.MULTIPLE_CAPTURE = None

    def select_piece(self, x: int, y: int) -> None:
        """
        Select a piece on the board.

        :param int x: x coordinate of the click position
        :param int y: y coordinate of the click position
        """

        if not self.SELECTED:
            for piece in self.pieces_sprites:
                if piece.rect.collidepoint(x, y):
                    if piece.data.player is self.player:
                        position = (piece.x, piece.y)
                        if position in self.PLAYER_MOVES:
                            # Log selected piece
                            position = (piece.x, piece.y)
                            logging.info(f"{piece.data} SELECTED at {position}")

                            # Highligh available moves to selected piece
                            self.SELECTED = piece
                            self._get_available_moves(self.SELECTED)

                        else:
                            logging.warning(
                                f"Can't select {piece.data}:"
                                f"there are pieces with capture moves."
                            )

                    else:
                        logging.warning(
                            f"Can't select piece from {Player(-self.player.value)} "
                            f"when current player is {self.player}!"
                        )

        else:
            for square in self.squares_sprites:
                if square.rect.collidepoint(x, y):
                    # Make move if move in allowed moves for selected piece
                    move = (square.row, square.col)
                    if move in self.next_moves.keys():
                        piece = self.SELECTED.data
                        position = (self.SELECTED.x, self.SELECTED.y)
                        self.board.move(
                            piece=piece,
                            old=position,
                            new=move,
                        )
                        logging.info(f"{piece} MOVED from {position} to {move}")

                        # Capture opponent piece
                        capture = self.next_moves.get(move)
                        if capture:
                            captured_piece = self.board.pieces[capture]
                            self.board.remove(pos=capture)
                            logging.info(f"{captured_piece} CAPTURED at {capture}")

                        # Update the board
                        self._update_board()

                        # Reset the board
                        self._reset_board()

                        # Handle multiple capture moves
                        if max([len(move) for move in self.PIECE_MOVES]) > 1:
                            # Force selecting multiple jump piece if path can continue
                            if move in self.PLAYER_MOVES:
                                # Next turn
                                self.next_turn(multiple_jump=True)
                                logging.info(
                                    f"Next turn: {self.turn} player: {self.player}"
                                )
                                # Select same piece with multiple jump
                                self.MULTIPLE_CAPTURE = (x, y)
                                self.select_piece(x, y)

                            else:
                                self.__stop_multiple_capture()

                        else:
                            self.__stop_multiple_capture()

                    elif self.MULTIPLE_CAPTURE:
                        logging.warning(
                            f"Move {move} not allowed! "
                            f"You need to complete the capture path."
                        )

                    else:
                        logging.warning(f"Move {move} not allowed!")
                        self._reset_board()

    def _opponent_move(self, path: list) -> None:
        """
        Make opponent moves based on path.

        :param list move: _description_
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

    def play(self):
        """
        Start the game environment.
        """
        clock = pygame.time.Clock()
        clock.tick(60)

        while not self.board.is_game_over():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Human player turn
                if self.player is self.HUMAN_PLAYER:
                    x, y = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.select_piece(x, y)

                    else:
                        # Regular hover
                        if not self.MULTIPLE_CAPTURE:
                            self.hover(x, y)

                        # Force focus when multiple capture
                        else:
                            x, y = self.MULTIPLE_CAPTURE
                            self.hover(x, y)

                # AI player turn
                else:
                    self._opponent_move(self.get_random_move(self.player))

                    self.next_turn()
                    logging.info(f"Next turn: {self.turn} player: {self.player}")

                    self._reset_board()
                    self._update_board()

            self.blink()

            self.squares_sprites.draw(self.screen)
            self.pieces_sprites.draw(self.screen)
            pygame.display.flip()

        print(self.stats)
