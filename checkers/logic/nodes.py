from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Node:
    """
    Node dataclass.

    Contains <captured>, <children>, and <position> attributes.
    """

    Square = tuple[int, int]

    position: Square
    captured: Square | None = field(default=None)
    children: list[Node] = field(default_factory=list)
