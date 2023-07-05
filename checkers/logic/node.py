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

    @staticmethod
    def get_readable_paths(paths: list) -> None:
        """
        Convert the given list of paths into readable defined paths.
        Print the readable paths.

        :param list[list[tuple]] paths: List of paths to be converted.
        """
        readable_paths = []
        move_description = None
        for path in paths:
            readable_path = []
            prev_position = path[0][0]

            for start, capture in path[1:]:
                if not capture and prev_position:
                    move_description = f"Move from {prev_position} to {start}"
                elif capture:
                    move_description = f"Capture from {capture} to {start}"

                prev_position = start

                if move_description:
                    readable_path.append(move_description)

            readable_paths.append(readable_path)

        for i, path in enumerate(readable_paths):
            print(f"Path {i + 1}:")
            for move in path:
                print(f"  - {move}")
