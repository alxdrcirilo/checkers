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
                    self.SELECTED_PIECE = piece_sprite
                    self.SELECTED_PIECE.focus(unselect=False)
                    self._get_available_moves(self.SELECTED_PIECE)
                    break

        else:
            for square_sprite in self.squares_sprites:
                if square_sprite.rect.collidepoint(x, y):
                    self.SELECTED_PIECE.focus(unselect=True)  # type: ignore

                    if (square_sprite.row, square_sprite.col) in self.next_moves.keys():
                        self.board.move(
                            piece=self.SELECTED_PIECE.data,  # type: ignore
                            old=(self.SELECTED_PIECE.x, self.SELECTED_PIECE.y),  # type: ignore
                            new=(square_sprite.row, square_sprite.col),
                        )

                        self.SELECTED_PIECE.x = square_sprite.row  # type: ignore
                        self.SELECTED_PIECE.y = square_sprite.col  # type: ignore
                        self.SELECTED_PIECE.move(  # type: ignore
                            left=self._get_coords(square_sprite.col),
                            top=self._get_coords(square_sprite.row),
                        )

                        captured_pos = self.next_moves.get(
                            (square_sprite.row, square_sprite.col)
                        )
                        if captured_pos:
                            self.board._remove(pos=captured_pos)
                            for piece_sprite in self.pieces_sprites:
                                if (piece_sprite.x, piece_sprite.y) == captured_pos:
                                    self.pieces_sprites.remove(piece_sprite)

                        self.SELECTED_PIECE = None

                        for square_sprite in self.squares_sprites:
                            square_sprite.reset()

                    else:
                        print("Not allowed")
                        self.SELECTED_PIECE = None
                        # Duplicated
                        for square_sprite in self.squares_sprites:
                            square_sprite.reset()

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
