import pygame

from checkers.graphics.constants import *


class SquareSprite(pygame.sprite.Sprite):
    def __init__(self, color, width, height, row, col):
        super().__init__()
        # Square
        self.color = color
        self.width = width
        self.height = height
        self.row = row
        self.col = col

        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, self.color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()

        self.text_offset = 4
        self._set_text(row, col)

    def _set_text(self, row: int, col: int):
        # Text (coordinates)
        color = WHITE if row % 2 != col % 2 else BLACK
        self.font = pygame.font.SysFont("Arial", 9)
        self.text_surface = self.font.render(f"{row},{col}", True, color)
        self.image.blit(
            self.text_surface,
            (self.text_offset, self.text_offset, self.width, self.height),
        )

    def reset(self) -> None:
        self.color = BROWN if self.row % 2 != self.col % 2 else WHITE
        self.update()

    def update(self) -> None:
        pygame.draw.rect(
            self.image, self.color, pygame.Rect(0, 0, self.width, self.height)
        )
        self._set_text(self.row, self.col)
