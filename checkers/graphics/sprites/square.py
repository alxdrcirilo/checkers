import pygame

from checkers.graphics.constants import *


class SquareSprite(pygame.sprite.Sprite):
    def __init__(self, color: str, width: int, height: int, row: int, col: int) -> None:
        """Initialize a SquareSprite object.

        :param str color: color of the square
        :param int width: width of the square
        :param int height: height of the square
        :param int row: row position of the square
        :param int col: column position of the square
        """
        super().__init__()

        # Square sprite properties
        self.color = color
        self.width = width
        self.height = height
        self.row = row
        self.col = col

        # Square
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, self.color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()

        # Text (coordinates)
        self.text_offset = 4
        self._set_text(row, col)

    def _set_text(self, row: int, col: int) -> None:
        """
        Set the text (coordinates) on the square.

        :param int row: row position of the square
        :param int col: column position of the square
        """
        color = WHITE if row % 2 != col % 2 else BLACK
        self.font = pygame.font.SysFont("Arial", 9)
        self.text_surface = self.font.render(f"{row},{col}", True, color)
        self.image.blit(
            self.text_surface,
            (self.text_offset, self.text_offset, self.width, self.height),
        )

    def reset(self) -> None:
        """
        Reset the square sprite.

        This method resets the square sprite to its default state.
        """
        self.color = BROWN if self.row % 2 != self.col % 2 else WHITE
        self.update()

    def update(self) -> None:
        """
        Update the square sprite.

        This method updates the appearance of the square sprite.
        """
        pygame.draw.rect(
            self.image, self.color, pygame.Rect(0, 0, self.width, self.height)
        )
        self._set_text(self.row, self.col)
