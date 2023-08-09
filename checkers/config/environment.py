import sys

import pygame

from checkers.graphics.sprites.piece import PieceSprite
from checkers.graphics.window import Window
from checkers.logic.piece import Player
from checkers.utils.logging import logging


class Environment(Window):
    """
    Environment class.

    Represents the game environment.
    """

    def __init__(self) -> None:
        """
        Initialize the environment.

        :ivar PLAYER_MOVES: list of pieces (positions) that the current player can move
        :ivar HUMAN_PLAYER: human player (BLACK piece)
        :ivar MULTIPLE_CAPTURE: (x, y) pixel coordinates of piece position if in multiple capture path
        :ivar SELECTED: currently selected game piece
        """
        self.clock = pygame.time.Clock()
        super().__init__()

        # Initialize instance variables
        self.PLAYER_MOVES: list = self.game.board.get_player_moves(self.game.player)
        self.HUMAN_PLAYER: Player = Player.BLACK
        self.MULTIPLE_CAPTURE: tuple | None = None
        self.SELECTED: PieceSprite | None = None

        # Set human player as starting player
        self.game.player = self.HUMAN_PLAYER
        logging.info(f"Started game with {self.game.player}")

    def __stop_multiple_capture(self) -> None:
        """
        Helper method to stop multiple capture.
        """
        self.game.next_turn()
        logging.info(f"Next turn: {self.game.turn} player: {self.game.player}")

        self.PLAYER_MOVES = self.game.board.get_player_moves(self.game.player)
        self.MULTIPLE_CAPTURE = None

    def select_piece(self, x: int, y: int) -> None:
        """
        Select a piece on the board.

        :param int x: x coordinate of the click position
        :param int y: y coordinate of the click position
        """

        if not self.SELECTED:
            for piece in self.pieces_sprites:
                if piece.rect.collidepoint(x, y):
                    if piece.data.player is self.game.player:
                        position = (piece.x, piece.y)
                        if position in self.PLAYER_MOVES:
                            # Log selected piece
                            position = (piece.x, piece.y)
                            logging.info(f"{piece.data} SELECTED at {position}")

                            # Highligh available moves to selected piece
                            self.SELECTED = piece
                            self._get_available_moves(self.SELECTED)

                        else:
                            logging.warning(
                                f"Can't select {piece.data}:"
                                f"there are pieces with capture moves."
                            )

                    else:
                        logging.warning(
                            f"Can't select piece from {Player(-self.game.player.value)} "
                            f"when current player is {self.game.player}!"
                        )

        else:
            for square in self.squares_sprites:
                if square.rect.collidepoint(x, y):
                    # Make move if move in allowed moves for selected piece
                    move = (square.row, square.col)
                    if move in self.next_moves.keys():
                        piece = self.SELECTED.data
                        position = (self.SELECTED.x, self.SELECTED.y)

                        # Slide piece
                        self._slide_piece(sprite=self.SELECTED, move=move)

                        # Move piece
                        self.game.board.move(
                            piece=piece,
                            old=position,
                            new=move,
                        )
                        logging.info(f"{piece} MOVED from {position} to {move}")

                        # Capture opponent piece
                        capture = self.next_moves.get(move)
                        if capture:
                            captured_piece = self.game.board.pieces[capture]
                            self.game.board.remove(pos=capture)
                            logging.info(f"{captured_piece} CAPTURED at {capture}")

                        # Update the board
                        self._update_board()

                        # Reset the board
                        self._reset_board()

                        # Handle multiple capture moves
                        if max([len(move) for move in self.PIECE_MOVES]) > 1:
                            # Force selecting multiple jump piece if path can continue
                            if move in self.PLAYER_MOVES:
                                # Next turn
                                self.game.next_turn(multiple_jump=True)
                                logging.info(
                                    f"Next turn: {self.game.turn} player: {self.game.player}"
                                )
                                # Select same piece with multiple jump
                                self.MULTIPLE_CAPTURE = (x, y)
                                self.select_piece(x, y)

                            else:
                                self.__stop_multiple_capture()

                        else:
                            self.__stop_multiple_capture()

                    elif self.MULTIPLE_CAPTURE:
                        logging.warning(
                            f"Move {move} not allowed! "
                            f"You need to complete the capture path."
                        )

                    else:
                        logging.warning(f"Move {move} not allowed!")
                        self._reset_board()

    def _make_move_ui(self, path: list) -> None:
        """
        Make opponent moves based on path (required for _slide_piece()).

        :param list path: move
        """
        while len(path) > 1:
            source, _ = path.pop(0)
            target, capture = path[0]

            # Slide piece
            x_source, y_source = list(map(lambda x: self._get_coords(x), source))
            for sprite in self.pieces_sprites:
                if sprite.rect.collidepoint(y_source, x_source):
                    self._slide_piece(sprite=sprite, move=target)

            # Move piece
            piece = self.game.board.pieces[source]
            self.game.board.move(piece=piece, old=source, new=target)
            logging.info(f"{piece} MOVED from {source} to {target}")

            # Cature
            if capture:
                captured_piece = self.game.board.pieces[capture]
                self.game.board.remove(pos=capture)
                logging.info(f"{captured_piece} CAPTURED at {capture}")

    def play(self) -> None:
        """
        Start the game environment.
        """
        while not self.game.is_game_over():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Human player turn
                if self.game.player is self.HUMAN_PLAYER:
                    x, y = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.select_piece(x, y)

                    else:
                        # Regular hover
                        if not self.MULTIPLE_CAPTURE:
                            self.hover(x, y)

                        # Force focus when multiple capture
                        else:
                            x, y = self.MULTIPLE_CAPTURE
                            self.hover(x, y)

                # AI player turn
                else:
                    # Random move
                    # self._make_move(self.get_random_move(self.game.player))

                    # Alpha-beta pruning move
                    ai_move = self.game.get_ai_move(player=self.game.player, depth=4)
                    self._make_move_ui(ai_move)

                    self.game.next_turn()
                    logging.info(
                        f"Next turn: {self.game.turn} player: {self.game.player}"
                    )

                    self._reset_board()
                    self._update_board()

            self.blink()

            self.squares_sprites.draw(self.screen)
            self.pieces_sprites.draw(self.screen)
            pygame.display.flip()

        while True:
            self.display_winner()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    pygame.quit()
                    sys.exit()
