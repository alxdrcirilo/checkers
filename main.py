from checkers.config.environment import Environment
from checkers.config.mock import MockGame
from checkers.logic.piece import Player


def main():
    checkers = Environment()
    checkers.play()

    # game = MockGame()
    # random_move = game.board._get_random_move(player=Player.BLACK)
    # print(random_move)


if __name__ == "__main__":
    main()
