from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Node:
    """
    Node dataclass.

    Contains <captured>, <children>, and <position> attributes.
    """

    position: tuple[int, int]
    captured: tuple[int, int] | None = field(default=None)
    children: list[Node] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"{self.position} {self.captured} 🡒 {self.children}"

    def _get_paths(self, node: Node | None = None) -> list:
        """
        Return all root-to-leaf paths.

        :param Node node: node (tree)
        :return list: list of root-to-leaf paths
        """
        if not node:
            node = self

        if not node.children:
            return [[(node.position, node.captured)]]

        else:
            paths = []
            for child in node.children:
                child_paths = self._get_paths(child)
                for child_path in child_paths:
                    paths.append([(node.position, node.captured)] + child_path)

            # Filter out free moves when jump moves available
            jumps = list(
                filter(
                    lambda x: [(jump, capture) for (jump, capture) in x if capture],
                    paths,
                )
            )
            if jumps:
                return jumps

            return paths
