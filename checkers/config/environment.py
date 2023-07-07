import sys

import pygame

from checkers.config.logging import logging
from checkers.graphics.sprites.piece import PieceSprite
from checkers.graphics.window import Window
from checkers.logic.piece import Player


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
        :ivar SELECTED_PIECE: currently selected game piece
        """
        super().__init__()

        # Initialize instance variables
        self.PLAYER_MOVES: list = self.board._get_player_moves(self.player)
        self.HUMAN_PLAYER: Player = Player.BLACK
        self.MULTIPLE_CAPTURE: tuple | None = None
        self.SELECTED_PIECE: PieceSprite | None = None

        # Set human player as starting player
        self.player = self.HUMAN_PLAYER
        logging.info(f"Started game with {self.HUMAN_PLAYER}")

    def select_piece(self, x: int, y: int) -> None:
        """
        Select a piece on the board.

        :param int x: x coordinate of the click position
        :param int y: y coordinate of the click position
        """
        if not self.SELECTED_PIECE:
            for piece_sprite in self.pieces_sprites:
                if piece_sprite.rect.collidepoint(x, y):
                    if piece_sprite.data.player is self.player:
                        piece_sprite_position = (piece_sprite.x, piece_sprite.y)
                        if piece_sprite_position in self.PLAYER_MOVES:
                            # Log selected piece
                            position = (piece_sprite.x, piece_sprite.y)
                            logging.info(f"{piece_sprite.data} SELECTED at {position}")

                            # Highligh available moves to selected piece
                            self.SELECTED_PIECE = piece_sprite
                            self._get_available_moves(self.SELECTED_PIECE)

                        else:
                            logging.warning(
                                f"Can't select piece {piece_sprite.data}. There are pieces with capture moves."
                            )

                    else:
                        logging.warning(
                            f"Can't select piece from {Player(-self.player.value)} when current player is {self.player}!"
                        )
                        self._reset_board()

        else:
            for square_sprite in self.squares_sprites:
                if square_sprite.rect.collidepoint(x, y):
                    # Make move if move in allowed moves for selected piece
                    move = (square_sprite.row, square_sprite.col)
                    if move in self.next_moves.keys():
                        piece = self.SELECTED_PIECE.data
                        pos = (self.SELECTED_PIECE.x, self.SELECTED_PIECE.y)
                        self.board.move(
                            piece=piece,
                            old=pos,
                            new=move,
                        )
                        logging.info(f"{piece} MOVED from {pos} to {move}")

                        # Capture opponent piece
                        captured_position = self.next_moves.get(move)
                        if captured_position:
                            captured_piece = self.board.pieces[captured_position]
                            self.board._remove(pos=captured_position)
                            logging.info(
                                f"{captured_piece} CAPTURED at {captured_position}"
                            )

                        # Update the board
                        self._update_board()

                        # Reset the board
                        self._reset_board()

                        # Get player moves
                        self.PLAYER_MOVES = self.board._get_player_moves(self.player)

                        # Handle multiple capture moves
                        if max([len(move) for move in self.piece_moves]) > 1:
                            # Force selecting multiple jump piece if path can continue
                            if move in self.PLAYER_MOVES:
                                # Next turn
                                self.next_turn(multiple_jump=True)
                                logging.info(
                                    f"Next turn: {self.turn} player: {self.player}"
                                )
                                # Select same piece with multiple jump
                                self.select_piece(x, y)
                                self.MULTIPLE_CAPTURE = (x, y)

                            else:
                                # Reset player to next player
                                self.next_turn()
                                logging.info(
                                    f"Next turn: {self.turn} player: {self.player}"
                                )
                                self.PLAYER_MOVES = self.board._get_player_moves(
                                    self.player
                                )
                                self.MULTIPLE_CAPTURE = None

                        else:
                            # Reset player to next player
                            self.next_turn()
                            logging.info(
                                f"Next turn: {self.turn} player: {self.player}"
                            )
                            self.PLAYER_MOVES = self.board._get_player_moves(
                                self.player
                            )
                            self.MULTIPLE_CAPTURE = None

                    elif self.MULTIPLE_CAPTURE:
                        logging.warning(
                            f"Move {move} not allowed! You need to complete the capture path."
                        )

                    else:
                        logging.warning(f"Move {move} not allowed!")
                        self._reset_board()

    def play(self):
        """
        Start the game environment.
        """
        clock = pygame.time.Clock()
        clock.tick(60)

        while not self.winner:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                x, y = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.select_piece(x, y)

                else:
                    if not self.MULTIPLE_CAPTURE:
                        self.hover(x, y)
                    else:
                        # If in multiple capture, force focus on piece
                        x, y = self.MULTIPLE_CAPTURE
                        self.hover(x, y)

            self.blink()

            self.squares_sprites.draw(self.screen)
            self.pieces_sprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
