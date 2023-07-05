from dataclasses import dataclass
from enum import Enum, unique


@unique
class Player(Enum):
    BLACK = -1
    WHITE = 1


@unique
class Rank(Enum):
    PAWN = 1
    KING = 2


@dataclass
class Piece:
    """
    Piece dataclass.

    Contains <player>, <rank>, and <cell> attributes.
    Contains <hash> and <symbol> properties:
        - <hash>: hash value for <player> + <rank> (e.g. 1)
        - <symbol>: string representation of piece (e.g. '⛂')
    """

    player: Player
    rank: Rank

    def __hash__(self) -> int:
        """
        Return hash value for a given piece.

        :return int: hash value
        """
        return self.player.value * self.rank.value

    @property
    def symbol(self) -> str:
        """
        Return <symbol> property.

        :return str | None: symbol representing the piece (e.g. '⛀')
        """
        mappings = {-2: "⛁", -1: "⛀", 1: "⛂", 2: "⛃"}
        return mappings[self.__hash__()]

    @property
    def directions(self) -> list[tuple[int, int]]:
        """
        Return moves a piece can make.

        :return list[tuple[int, int]]: list of allowed moves
        """
        dir = {
            Rank.PAWN: {(self.player.value, -1), (self.player.value, 1)},
            Rank.KING: {(-1, -1), (-1, 1), (1, -1), (1, 1)},
        }

        return list(dir[self.rank])
