from pathlib import Path

import pygame

from checkers.logic.piece import Piece


class PieceSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        color: str,
        size: int,
        left: int,
        top: int,
        x: int,
        y: int,
        data: Piece,
    ) -> None:
        """
        Initialize a PieceSprite object.

        :param str color: color of the piece
        :param int piece_size: size of the piece
        :param int left: left position of the piece
        :param int top: top position of the piece
        :param int x: x coordinate of the piece
        :param int y: y coordinate of the piece
        :param Piece data: piece
        """
        super().__init__()

        # Piece sprite properties
        self.color = color
        self.data = data
        self.size = [size, size]
        self.x = x
        self.y = y

        # Asset
        path = Path("assets/images")
        file = path / f"{self.data.rank.name.lower()}_{self.color}.png"
        self.image = pygame.image.load(file)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = pygame.Rect(left, top, size, size)

    def focus(self, unselect: bool = True) -> None:
        """
        Click on a piece sprite and change its image to show focus.

        :param PieceSprite piece: the sprite representing the piece
        :param bool unselect: indicates whether to unselect the piece
        """
        path = Path("assets/images")
        hover = "" if unselect else "_hover"
        file = path / f"{self.data.rank.name.lower()}_{self.color}{hover}.png"
        self.image = pygame.image.load(file)
        self.image = pygame.transform.scale(self.image, self.size)
