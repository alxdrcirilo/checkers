from copy import deepcopy
from math import inf

from checkers.logic.piece import Player, Rank


class AlphaBetaPruning:
    def evaluate(self, game, max_player: Player) -> int:
        """
        Evaluate the game state for the specified player.

        :param Game game: current game state
        :param Player max_player: maximizing player
        :return int: evaluation score for the given game state
        """
        score = 0
        for player in [Player.BLACK, Player.WHITE]:
            for rank in [Rank.PAWN, Rank.KING]:
                pieces = dict(
                    filter(
                        lambda x: x[1].player is player and x[1].rank is rank,
                        game.board.pieces.items(),
                    )
                )

                pieces_score = len(pieces) * rank.value

                if player is max_player:
                    score += pieces_score
                else:
                    score -= pieces_score

        return int(score)

    def minimax(
        self,
        game,
        depth: int,
        maximizer: bool,
        max_player: Player,
        alpha: float = -inf,
        beta: float = inf,
    ) -> tuple[list | None, float]:
        """
        Perform the alpha-beta pruning minimax search to find the best move.

        :param Game game: current game state
        :param int depth: depth of the search tree
        :param bool maximizer: True if it's the maximizing player's turn, False otherwise
        :param Player max_player: maximizing player
        :param float alpha: alpha value for alpha-beta pruning
        :param float beta: beta value for alpha-beta pruning
        :return tuple[list | None, float]: best move found by the search and its evaluation score
        """
        if depth == 0 or game.is_game_over():
            score = self.evaluate(game, max_player)
            return None, score

        if maximizer:
            best_score = -inf

            for piece in game.board.get_player_moves(game.player):
                move = game.board._get_player_tree(game.player)[piece][0]
                move_copy = deepcopy(move)

                game_copy = deepcopy(game)
                game_copy._make_move(move)
                game_copy.next_turn()

                score = self.minimax(
                    game_copy, depth - 1, False, max_player, alpha, beta
                )[1]

                if score > best_score:
                    best_score = score
                    best_move = move_copy

                if alpha and beta:
                    alpha = max(alpha, score)
                    if alpha >= beta:
                        break

            return best_move, best_score

        else:
            best_score = inf

            for piece in game.board.get_player_moves(game.player):
                move = game.board._get_player_tree(game.player)[piece][0]
                move_copy = deepcopy(move)

                game_copy = deepcopy(game)
                game_copy._make_move(move)
                game_copy.next_turn()

                score = self.minimax(
                    game_copy, depth - 1, True, max_player, alpha, beta
                )[1]

                if score < best_score:
                    best_score = score
                    best_move = move_copy

                if alpha and beta:
                    beta = min(beta, score)
                    if alpha >= beta:
                        break

            return best_move, best_score
