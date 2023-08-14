from pathlib import Path

import pygame

from checkers.graphics.constants import *
from checkers.graphics.sprites.piece import PieceSprite
from checkers.graphics.sprites.square import SquareSprite
from checkers.logic.game import Game
from checkers.logic.piece import Piece

pygame.init()
pygame.display.set_caption("Checkers")
pygame.display.set_icon(pygame.image.load(Path("assets/icons/checkers.png")))


class Window:
    """
    Window class.

    Represents the window of the game.
    """

    def __init__(self, resolution=512) -> None:
        """
        Initializes the Window class.

        :param int resolution: size of the game, defaults to 512 pixels
        :ivar game: game
        :ivar BLINK_INTERVAL: interval (in milliseconds) for blinking
        :ivar HIGHLIGHT_SQUARE: indicates whether squares should be highlighted
        :ivar TIMER: timer value
        :ivar size: size of the window
        :ivar screen: pygame screen object
        :ivar pieces: pygame sprite group for game pieces
        :ivar squares: pygame sprite group for squares
        """
        self.game = Game()
        self.clock = pygame.time.Clock()
        self.clock.tick(60)

        # Blinking variables
        self.BLINK_INTERVAL = 300
        self.HIGHLIGHT_SQUARE = True
        self.TIMER = 0

        # Setup screen
        self.size = [resolution + 9 * BORDER_WIDTH] * 2
        self.screen = pygame.display.set_mode(self.size)

        # Setup sprites
        self.pieces_sprites = pygame.sprite.Group()
        self.squares_sprites = pygame.sprite.Group()

        self.__get_squares_sprites()
        self.__get_pieces_sprites()
        self._draw_board()

    @staticmethod
    def _get_coords(x: int) -> int:
        """
        Get the coordinates in pixels based on the row|column (x) for a piece sprite.

        :param int x: row or column index (e.g. 2)
        :return int: pixel position
        """
        return SIZE * x + BORDER_WIDTH * x + BORDER_WIDTH + SIZE // 2 - PIECE_SIZE // 2

    def _draw_board(self) -> None:
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

    def _update_board(self) -> None:
        """
        Update the board based on its state.

        Clears all piece sprites.
        Gets new piece sprites based on new board state.
        Draws new piece sprites.
        """
        self.pieces_sprites.empty()
        self.__get_pieces_sprites()
        self.pieces_sprites.draw(self.screen)

    def _reset_board(self) -> None:
        """
        Reset the board based on its state.

        Clears highlighted moves.
        Unselects focused pieces.
        Get new allowed player moves.
        """
        self.SELECTED = None
        self.PLAYER_MOVES = self.game.board.get_player_moves(self.game.player)
        for square_sprite in self.squares_sprites:
            square_sprite.reset()

    def __get_squares_sprites(self) -> None:
        """
        Create and add square sprites to the sprite group.
        """
        for row, col in self.game.board._state:
            color = BROWN if row % 2 != col % 2 else WHITE
            left = BORDER_WIDTH + SIZE * col + BORDER_WIDTH * col
            top = BORDER_WIDTH + SIZE * row + BORDER_WIDTH * row

            square_sprite = SquareSprite(color, SIZE, SIZE, row, col)
            square_sprite.rect.x = left
            square_sprite.rect.y = top
            self.squares_sprites.add(square_sprite)

    def __get_pieces_sprites(self) -> None:
        """
        Create and add piece sprites to the sprite group.
        """
        for (row, col), node in self.game.board._state.items():
            if type(node) is Piece:
                piece = node
                color = piece.player.name.lower()
                piece_sprite = PieceSprite(
                    color=color,
                    size=PIECE_SIZE,
                    left=self._get_coords(col),
                    top=self._get_coords(row),
                    x=row,
                    y=col,
                    data=piece,
                )
                self.pieces_sprites.add(piece_sprite)

    def _get_available_moves(self, piece_sprite: PieceSprite) -> None:
        """
        Get available moves for a given piece sprite.

        :param PieceSprite piece_sprite: the sprite representing the piece
        """

        # Get moves (paths) that selected piece can make
        self.PIECE_MOVES = self.game.board._get_player_tree(piece_sprite.data.player)[
            (piece_sprite.x, piece_sprite.y)
        ]

        # Get imminent next moves
        self.next_moves = {}
        for move in self.PIECE_MOVES:
            jump, capture = move.pop(1)
            self.next_moves[jump] = capture

        # Change square sprite(s) color attributes based on type of move (JUMP or CAPTURE)
        for jump, capture in self.next_moves.items():
            jump_x, jump_y = self._get_coords(jump[1]), self._get_coords(jump[0])

            for square_sprite in self.squares_sprites:
                if square_sprite.rect.collidepoint(jump_x, jump_y):
                    square_sprite.color = JUMP
                    break

            if capture:
                capture_x, capture_y = self._get_coords(capture[1]), self._get_coords(
                    capture[0]
                )
                for square_sprite in self.squares_sprites:
                    if square_sprite.rect.collidepoint(capture_x, capture_y):
                        square_sprite.color = CAPTURE
                        break

            # Update board
            self.squares_sprites.update()
            self.squares_sprites.draw(self.screen)
            self.pieces_sprites.draw(self.screen)

    def blink(self) -> None:
        """
        Blink available moves for selected piece.
        """
        if self.SELECTED:
            current_time = pygame.time.get_ticks()
            if current_time - self.TIMER >= self.BLINK_INTERVAL:
                self.HIGHLIGHT_SQUARE = not self.HIGHLIGHT_SQUARE
                self.TIMER = current_time

            if self.HIGHLIGHT_SQUARE:
                self._get_available_moves(self.SELECTED)
            else:
                for square in self.squares_sprites:
                    square.reset()

    def hover(self, x: int, y: int) -> None:
        """
        Hover a piece on the board and focus if piece belongs to current player.

        :param int x: x coordinate of the hovered position
        :param int y: y coordinate of the hovered position
        """
        moves = self.game.board.get_player_moves(self.game.player)
        for piece_sprite in self.pieces_sprites:
            if piece_sprite.rect.collidepoint(x, y):
                piece_sprite_position = (piece_sprite.x, piece_sprite.y)
                if (
                    piece_sprite.data.player is self.game.player
                    and piece_sprite_position in moves
                ):
                    piece_sprite.focus(unselect=False)
            else:
                piece_sprite.focus(unselect=True)

    def _slide_piece(self, sprite: PieceSprite, move: tuple) -> None:
        """
        Moving piece animation.
        67 pixels apart per row/column.

        :param PieceSprite sprite: piece sprite
        :param tuple move: position to move to
        """
        start_x = self._get_coords(sprite.x)
        start_y = self._get_coords(sprite.y)
        end_x = self._get_coords(move[0])
        end_y = self._get_coords(move[1])

        fps = 67 * abs(sprite.x - move[0])
        delta = 1

        for _ in range(fps):
            if end_x - start_x > 0:
                sprite.rect.top += delta
            else:
                sprite.rect.top -= delta

            if start_y - end_y > 0:
                sprite.rect.left -= delta
            else:
                sprite.rect.left += delta

            self._draw_board()
            self.squares_sprites.draw(self.screen)
            self.pieces_sprites.draw(self.screen)

            self.clock.tick(fps * 3)
            pygame.display.flip()

    def display_winner(self) -> None:
        # Text
        font = pygame.font.Font("assets/fonts/OpenSans-Medium.ttf", 24)
        text = font.render(f"Winner: {self.game.winner}", True, WHITE)

        # Rect
        width = text.get_width() + 180
        height = text.get_height() + 140
        rect = pygame.Rect(
            (self.screen.get_height() - width) // 2,
            (self.screen.get_height() - height) // 2,
            width,
            height,
        )

        # Draw textbox
        pygame.draw.rect(self.screen, GRAY, rect)

        # Calculate the position to center the text within the textbox
        text_x = rect.centerx - text.get_width() // 2
        text_y = rect.centery - text.get_height() // 2
        self.screen.blit(text, (text_x, text_y))

        # Turn text
        font = pygame.font.Font("assets/fonts/OpenSans-Medium.ttf", 20)
        text = font.render(f"Turn: {self.game.turn}", True, WHITE)
        text_x = rect.centerx - text.get_width() // 2
        self.screen.blit(text, (text_x, text_y - 34))

        # "Click anywhere to exit" text
        font = pygame.font.Font("assets/fonts/OpenSans-Medium.ttf", 12)
        text = font.render(f"Press any keystroke to exit", True, WHITE)
        text_x = rect.centerx - text.get_width() // 2
        self.screen.blit(text, (text_x, text_y + 40))
