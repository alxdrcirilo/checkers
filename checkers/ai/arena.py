from checkers.ai.ab_pruning import AlphaBetaPruning
from checkers.logic.game import Game
from checkers.logic.piece import Player
from checkers.utils.logging import logging


class Arena:
    """
    Arena class.

    Represents the arena where we can run games.
    """

    def play(self, games: int, depth: int) -> tuple[int, int]:
        """
        Playout <games>.

        :param int games: number of games to play
        :param int depth: depth for the minimax algorithm
        :return tuple[int, int]: (BLACK player wins, WHITE player wins)
        """

        wins = {Player.BLACK: 0, Player.WHITE: 0}

        for _ in range(games):
            game = Game()

            while not game.is_game_over():
                # Random player turn
                if game.player is Player.BLACK:
                    game._make_move(game.get_random_move(game.player))
                    game.next_turn()
                    logging.info(f"Next turn: {game.turn} player: {game.player}")

                # AI player turn
                else:
                    ai = AlphaBetaPruning()
                    if depth > 0:
                        best_move, _ = ai.minimax(
                            game=game,
                            depth=depth,
                            maximizer=True,
                            max_player=game.player,
                        )
                    elif depth == 0:
                        best_move = game.get_random_move(game.player)

                    game._make_move(best_move)  # type: ignore
                    game.next_turn()
                    logging.info(f"Next turn: {game.turn} player: {game.player}")

            wins[game.winner] += 1  # type: ignore

        return wins[Player.BLACK], wins[Player.WHITE]
