from pathlib import Path

import pygame

from checkers.config.mock import MockGame
from checkers.graphics.constants import *
from checkers.graphics.sprites.piece import PieceSprite
from checkers.graphics.sprites.square import SquareSprite
from checkers.logic.piece import Piece

pygame.init()
pygame.display.set_caption("Checkers")
pygame.display.set_icon(pygame.image.load(Path("assets/icons/checkers.png")))


class Window(MockGame):
    def __init__(self, resolution=512) -> None:
        super().__init__()

        self.size = [resolution + 9 * BORDER_WIDTH] * 2
        self.screen = pygame.display.set_mode(self.size)

        self.BLINK_INTERVAL = 400
        self.HIGHLIGHT_SQUARE = True
        self.SELECTED_PIECE = None
        self.TIMER = 0

        self.pieces = pygame.sprite.Group()
        self.squares = pygame.sprite.Group()

        self._get_squares()
        self._get_pieces()
        self._draw_board()

    def _draw_board(self):
        def _get_coords(x: int):
            return BORDER_WIDTH + SIZE * x + BORDER_WIDTH * x

        # Fill
        self.screen.fill(WHITE)
        self.squares.draw(self.screen)

        # Outline
        for row in range(9):
            for col in range(9):
                width = BORDER_WIDTH - 1
                left = _get_coords(col)
                top = _get_coords(row)

                # Square borders (vertical)
                start = (left + SIZE, top + SIZE)
                end = (left + SIZE, top)
                pygame.draw.line(self.screen, GRAY, start, end, width)

                # Square borders (horizontal)
                start = (left, top + SIZE)
                end = (left + SIZE, top + SIZE)
                pygame.draw.line(self.screen, GRAY, start, end, width)

    def _get_squares(self):
        for row, col in self.board._state:
            color = BROWN if row % 2 != col % 2 else WHITE
            left = BORDER_WIDTH + SIZE * col + BORDER_WIDTH * col
            top = BORDER_WIDTH + SIZE * row + BORDER_WIDTH * row

            square_sprite = SquareSprite(color, SIZE, SIZE, row, col)
            square_sprite.rect.x = left
            square_sprite.rect.y = top
            self.squares.add(square_sprite)

    @staticmethod
    def __get_coords(x: int):
        return SIZE * x + BORDER_WIDTH * x + BORDER_WIDTH + SIZE // 2 - PIECE_SIZE // 2

    def _get_pieces(self):
        for (row, col), node in self.board._state.items():
            if type(node) is Piece:
                piece = node
                color = piece.player.name.lower()
                piece_sprite = PieceSprite(
                    color=color,
                    piece_size=PIECE_SIZE,
                    left=self.__get_coords(col),
                    top=self.__get_coords(row),
                    x=row,
                    y=col,
                    data=piece,
                )
                self.pieces.add(piece_sprite)

    def _draw_rect(self, row: int, col: int, color: str):
        """
        Draws a pygame.Rect object highlighting captured pieces and/or jumps.
        """
        left = BORDER_WIDTH + SIZE * col + BORDER_WIDTH * col
        top = BORDER_WIDTH + SIZE * row + BORDER_WIDTH * row
        offset = 2
        pygame.draw.rect(
            surface=self.screen,
            color=color,
            rect=pygame.Rect(
                left + offset,
                top + offset,
                SIZE - offset * 1.5,
                SIZE - offset * 1.5,
            ),
            width=2,
        )

    def __get_available_moves(self, piece_sprite: PieceSprite):
        available_moves = self.board._get_player_moves(
            player=piece_sprite.data.player,
            position=(piece_sprite.x, piece_sprite.y),
        )[(piece_sprite.x, piece_sprite.y)]

        # print(f"{available_moves=}")
        self.next_moves = {}
        for move in available_moves:
            jump, capture = move.pop(1)
            self.next_moves[jump] = capture
        # print(f"{self.next_moves=}")

        for jump, capture in self.next_moves.items():
            jump_x, jump_y = self.__get_coords(jump[1]), self.__get_coords(jump[0])

            for square in self.squares:
                if square.rect.collidepoint(jump_x, jump_y):
                    square.color = JUMP
                    break

            if capture:
                capture_x, capture_y = self.__get_coords(capture[1]), self.__get_coords(
                    capture[0]
                )
                for square in self.squares:
                    if square.rect.collidepoint(capture_x, capture_y):
                        square.color = CAPTURE
                        break

            self.squares.update()
            self.squares.draw(self.screen)
            self.pieces.draw(self.screen)

    # TODO: put this in piece.py sprite
    def __click_piece(self, piece: PieceSprite, unselect: bool = True):
        path = Path("assets/images")
        hover = "" if unselect else "_hover"
        file = path / f"{piece.rank}_{piece.color}{hover}.png"
        piece.image = pygame.image.load(file)
        piece.image = pygame.transform.scale(piece.image, [PIECE_SIZE, PIECE_SIZE])

    def select_piece(self, x, y):
        if not self.SELECTED_PIECE:
            for piece in self.pieces:
                if piece.rect.collidepoint(x, y):
                    self.SELECTED_PIECE = piece
                    self.__click_piece(piece=self.SELECTED_PIECE, unselect=False)
                    self.__get_available_moves(self.SELECTED_PIECE)
                    break
        else:
            for square in self.squares:
                if square.rect.collidepoint(x, y):
                    self.__click_piece(piece=self.SELECTED_PIECE, unselect=True)

                    if (square.row, square.col) in self.next_moves.keys():
                        self.board.move(
                            piece=self.SELECTED_PIECE.data,
                            old=(self.SELECTED_PIECE.x, self.SELECTED_PIECE.y),
                            new=(square.row, square.col),
                        )

                        self.SELECTED_PIECE.x = square.row
                        self.SELECTED_PIECE.y = square.col
                        self.SELECTED_PIECE.move(
                            left=self.__get_coords(square.col),
                            top=self.__get_coords(square.row),
                            piece_size=PIECE_SIZE,
                        )

                        captured_pos = self.next_moves.get((square.row, square.col))
                        if captured_pos:
                            self.board._remove(pos=captured_pos)
                            for piece in self.pieces:
                                if (piece.x, piece.y) == captured_pos:
                                    self.pieces.remove(piece)

                        self.SELECTED_PIECE = None

                        for square in self.squares:
                            square.reset()

                    else:
                        print("Not allowed")
                        self.SELECTED_PIECE = None
                        # Duplicated
                        for square in self.squares:
                            square.reset()

    def blink(self):
        if self.SELECTED_PIECE:
            current_time = pygame.time.get_ticks()
            if current_time - self.TIMER >= self.BLINK_INTERVAL:
                self.HIGHLIGHT_SQUARE = not self.HIGHLIGHT_SQUARE
                self.TIMER = current_time

            if self.HIGHLIGHT_SQUARE:
                self.__get_available_moves(self.SELECTED_PIECE)
            else:
                for square in self.squares:
                    square.reset()
