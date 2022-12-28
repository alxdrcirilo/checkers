from checkers.game import Game


def main():
    game = Game()
    game.play()
    print(f"{game.winner=}")


if __name__ == "__main__":
    main()
