from checkers.logic.game import Game
from checkers.ui.mainwindow import Window


def main():
    game = Game()
    # game.play()
    # print(f"{game.winner=}")

    ui = Window(game)
    ui.show()


if __name__ == "__main__":
    main()
