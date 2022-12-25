from checkers.game import Game


def main():
    game = Game()

    print(game.board.pieces)
    print(game.board)
    print(game.player)
    print(game.players)
    print(game.winner)

    # print(game.board.get_player_moves(player=game.player))


if __name__ == "__main__":
    main()
