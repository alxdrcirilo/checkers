import sys

import pygame

from checkers.config.logging import logging
from checkers.graphics.sprites.piece import PieceSprite
from checkers.graphics.window import Window


class Environment(Window):
    """
    Environment class.

    Represents the game environment.
    """

    def __init__(self) -> None:
        """
        Initialize the environment.

        :ivar SELECTED_PIECE: currently selected game piece
        """
        super().__init__()
        logging.info(f"Started game with {self.player}")
        self.SELECTED_PIECE: PieceSprite | None = None

    def select_piece(self, x: int, y: int) -> None:
        """
        Select a piece on the board.

        :param int x: x coordinate of the click position
        :param int y: y coordinate of the click position
        """
        if not self.SELECTED_PIECE:
            for piece_sprite in self.pieces_sprites:
                if piece_sprite.rect.collidepoint(x, y):
                    # Log selected piece
                    position = (piece_sprite.x, piece_sprite.y)
                    logging.info(f"{piece_sprite.data} SELECTED at {position}")

                    # Highligh available moves to selected piece
                    self.SELECTED_PIECE = piece_sprite
                    self.SELECTED_PIECE.focus(unselect=False)
                    self._get_available_moves(self.SELECTED_PIECE)

        else:
            for square_sprite in self.squares_sprites:
                if square_sprite.rect.collidepoint(x, y):
                    # Unselect piece
                    self.SELECTED_PIECE.focus(unselect=True)  # type: ignore

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

                        captured_position = self.next_moves.get(move)
                        if captured_position:
                            captured_piece = self.board.pieces[captured_position]
                            self.board._remove(pos=captured_position)
                            logging.info(
                                f"{captured_piece} CAPTURED at {captured_position}"
                            )

                        # Update the pygame board
                        self._update_board()
                        self._reset_board()

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

            self.blink()

            self.squares_sprites.draw(self.screen)
            self.pieces_sprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
