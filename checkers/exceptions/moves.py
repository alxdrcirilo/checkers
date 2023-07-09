from checkers.logic.piece import Player


class NoMoves(Exception):
    def __init__(self, player: Player) -> None:
        super().__init__(f"{player} ran out of moves")
