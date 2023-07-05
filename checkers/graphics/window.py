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
    """
    Window class.

    Represents the window of the game.
    This class extends the MockGame class.
    """

    def __init__(self, resolution=512) -> None:
        """
        Initializes the Window class.

        :param int resolution: size of the game, defaults to 512 pixels
        :ivar BLINK_INTERVAL: The interval (in milliseconds) for blinking
        :ivar HIGHLIGHT_SQUARE: Indicates whether squares should be highlighted
        :ivar SELECTED_PIECE: The currently selected game piece
        :ivar TIMER: The timer value
        :ivar size: The size of the window
        :ivar screen: The pygame screen object
        :ivar pieces: The pygame sprite group for game pieces
        :ivar squares: The pygame sprite group for squares
        """
        super().__init__()

        # Blinking variables
        self.BLINK_INTERVAL = 400
        self.HIGHLIGHT_SQUARE = True
        self.SELECTED_PIECE = None
        self.TIMER = 0

        # Setup screen
        self.size = [resolution + 9 * BORDER_WIDTH] * 2
        self.screen = pygame.display.set_mode(self.size)

        # Setup sprites
        self.pieces = pygame.sprite.Group()
        self.squares = pygame.sprite.Group()

        self.__get_squares()
        self.__get_pieces()
        self.__draw_board()

    @staticmethod
    def __get_coords(x: int) -> int:
        """
        Get the coordinates in pixels based on the row|column (x) for a piece sprite.

        :param int x: row or column index (e.g. 2)
        :return int: pixel position
        """
        return SIZE * x + BORDER_WIDTH * x + BORDER_WIDTH + SIZE // 2 - PIECE_SIZE // 2

    def __draw_board(self) -> None:
        """
        Draw the board.

        Fills the boards.
        Add square borders.
        """

        def _get_coords(x: int) -> int:
            """
            Get the coordinates in pixels based on the row|column (x) for a square sprite.

            :param int x: row or column index (e.g. 2)
            :return int: pixel position
            """
            return BORDER_WIDTH + SIZE * x + BORDER_WIDTH * x

        # Fill
        self.screen.fill(WHITE)

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

    def __get_squares(self) -> None:
        """
        Create and add square sprites to the sprite group.
        """
        for row, col in self.board._state:
            color = BROWN if row % 2 != col % 2 else WHITE
            left = BORDER_WIDTH + SIZE * col + BORDER_WIDTH * col
            top = BORDER_WIDTH + SIZE * row + BORDER_WIDTH * row

            square_sprite = SquareSprite(color, SIZE, SIZE, row, col)
            square_sprite.rect.x = left
            square_sprite.rect.y = top
            self.squares.add(square_sprite)

    def __get_pieces(self) -> None:
        """
        Create and add piece sprites to the sprite group.
        """
        for (row, col), node in self.board._state.items():
            if type(node) is Piece:
                piece = node
                color = piece.player.name.lower()
                piece_sprite = PieceSprite(
                    color=color,
                    size=PIECE_SIZE,
                    left=self.__get_coords(col),
                    top=self.__get_coords(row),
                    x=row,
                    y=col,
                    data=piece,
                )
                self.pieces.add(piece_sprite)

    def __get_available_moves(self, piece_sprite: PieceSprite) -> None:
        """
        Get available moves for a given piece sprite.

        :param PieceSprite piece_sprite: the sprite representing the piece
        """
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

    def select_piece(self, x: int, y: int) -> None:
        """
        Select a piece on the board.

        :param int x: x coordinate of the click position
        :param int y: y coordinate of the click position
        """
        if not self.SELECTED_PIECE:
            for piece in self.pieces:
                if piece.rect.collidepoint(x, y):
                    self.SELECTED_PIECE = piece
                    self.SELECTED_PIECE.focus(unselect=False)
                    self.__get_available_moves(self.SELECTED_PIECE)
                    break
        else:
            for square in self.squares:
                if square.rect.collidepoint(x, y):
                    self.SELECTED_PIECE.focus(unselect=True)

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

    def blink(self) -> None:
        """
        Blink available moves for selected piece.
        """
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
