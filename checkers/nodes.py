class Node:
    def __init__(
        self,
        position: tuple[int, int] = (0, 0),
        capture: bool = False,
    ) -> None:
        self.parent = None
        self.position = position
        self.children = list()
        self.capture = capture

    def add(self, child) -> None:
        self.children.append(child)
        child.parent = self
