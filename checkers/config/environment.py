import sys

import pygame

from checkers.graphics.window import Window


class Environment(Window):
    def __init__(self) -> None:
        super().__init__()

    def show(self):
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

            self.squares.draw(self.screen)
            self.pieces.draw(self.screen)
            pygame.display.flip()

        pygame.quit()