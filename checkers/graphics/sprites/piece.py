from pathlib import Path

import pygame


# TODO: add typehints
class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, color, piece_size, left, top, x, y, data):
        super().__init__()
        self.color = color
        self.rank = data.rank.name.lower()
        path = Path("assets/images")
        file = path / f"{self.rank}_{self.color}.png"
        self.image = pygame.image.load(file)
        self.image = pygame.transform.scale(self.image, [piece_size, piece_size])
        self.rect = pygame.Rect(left, top, piece_size, piece_size)
        self.data = data
        self.x = x
        self.y = y

    def move(self, left: int, top: int, piece_size: int):
        self.rect = pygame.Rect(left, top, piece_size, piece_size)
