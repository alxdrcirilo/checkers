import time
from pathlib import Path

import pygame
from pygame.locals import QUIT

from checkers.logic.game import Game
from checkers.logic.nodes import Node
from checkers.logic.piece import Piece

pygame.init()
pygame.display.set_caption("Checkers")
clock = pygame.time.Clock()
clock.tick(60)


BLACK = (40, 40, 40)
BROWN = (150, 100, 50)
DARKBROWN = (120, 70, 20)
DARKGRAY = (50, 50, 50)
GRAY = (180, 180, 180)
WHITE = (215, 215, 215)

# TODO: Cleanup
class SquareSprite(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super().__init__()

        # Squares
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()

        # Text
        color, offset = WHITE if x % 2 != y % 2 else BLACK, 2
        self.font = pygame.font.SysFont("Arial", 10)
        self.text_surface = self.font.render(f"{x},{y}", True, color)
        self.image.blit(self.text_surface, (offset, offset, width, height))


# TODO: Cleanup
class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, color, width, height, row, col, data):
        super().__init__()

        self.color = color
        self.rank = data.rank.name.lower()
        path = Path("checkers/assets")
        file = path / f"{self.rank}_{self.color}.png"

        self.image = pygame.image.load(file)
        self.rect = pygame.Rect(width, height, 64, 64)

        self.data = data
        self.x = row
        self.y = col


# TODO: Cleanup
class Window:
    def __init__(self, game: Game, resolution=640) -> None:
        self.game = game
        self.res = resolution
        self._setup()

    def _setup(self):
        self.screen = pygame.display.set_mode([self.res] * 2)
        self.screen.fill(DARKGRAY)

        # Board
        colors = [BLACK, DARKBROWN, DARKGRAY]
        for offset, color in enumerate(colors):
            width, height = [self.res * 0.88 - (offset + 1) * 10] * 2
            left, top = [(self.res - width) // 2] * 2
            rect = pygame.Rect(left, top, width + 2, height + 2)
            pygame.draw.rect(self.screen, color, rect, border_radius=10)

        # Sprites (squares and coordinates)
        self.squares = pygame.sprite.Group()
        self.texts = pygame.sprite.Group()
        for x, y in self.game.board._state:
            color = BLACK if x % 2 != y % 2 else WHITE
            width, height = [512 // 8] * 2
            left = (self.res - 512) // 2 + width * y
            top = (self.res - 512) // 2 + height * x

            object_ = SquareSprite(color, width, height, x, y)
            object_.rect.x = left
            object_.rect.y = top
            self.squares.add(object_)

    def show(self):
        while not self.game.winner:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

                # TODO: Cleanup
                # self.game.random_move()
                # time.sleep(0.5)
                # self.game.next_turn()

                self.squares.draw(self.screen)

                x, y = pygame.mouse.get_pos()

                # Pieces
                self.pieces = pygame.sprite.Group()
                for (row, col), node in self.game.board._state.items():
                    dim = 512 // 8
                    left = dim + dim * col
                    top = dim + dim * row

                    if type(node) is Piece:
                        piece = node
                        color = piece.player.name.lower()
                        object_ = PieceSprite(color, left, top, row, col, piece)
                        self.pieces.add(object_)

                # Borders
                for row in range(9):
                    for col in range(9):
                        dim = 512 // 8
                        left = dim + dim * col
                        top = dim + dim * row
                        # Square borders (vertical)
                        if row in [0, 1]:
                            start = (left - 1, top - 64 * row)
                            end = (left - 1, top + 512 - 64 * row)
                            pygame.draw.line(self.screen, BLACK, start, end, 2)

                        # Square borders (horizontal)
                        if col in [0, 1]:
                            start = (left - 1 - col * 64, top)
                            end = (left - 1 + 512 - col * 64, top)
                            pygame.draw.line(self.screen, BLACK, start, end, 2)

                # Hover
                for piece in self.pieces:
                    if piece.rect.collidepoint(x, y):
                        path = Path("checkers/assets")
                        file = path / f"{piece.rank}_{piece.color}_hover.png"
                        piece.image = pygame.image.load(file)

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print(f"Clicked on {piece.data} at {piece.x},{piece.y}")
                            pos = (piece.x, piece.y)
                            root = Node(pos)
                            node = self.game.board.get_moves(pos, root)

                            for child in node.children:
                                print(child.position)
                                row, col = child.position
                                dim = 512 // 8
                                left = dim + dim * col + 1
                                top = dim + dim * row
                                self.image = pygame.Surface([dim] * 2)
                                pygame.draw.rect(
                                    self.screen,
                                    (100, 100, 150),
                                    pygame.Rect(left, top + 2, dim - 2, dim - 2),
                                )
                                self.pieces.update()

                self.pieces.draw(self.screen)
                pygame.display.flip()
