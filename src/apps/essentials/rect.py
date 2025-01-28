import numpy as np

from .pos import Pos


class Rect:
    def __init__(self, x: int, y: int, width: int, height: int):
        assert width > 0 and height > 0
        self.width, self.height = width, height
        self.x, self.y = x, y

    def move(self, vector: Pos) -> "Rect":
        return Rect(self.x + vector.x, self.y + vector.y, self.width, self.height)

    def pos(self) -> Pos:
        return Pos(self.x, self.y)

    def to_tuple(self) -> tuple[int, int, int, int]:
        return self.x, self.y, self.width, self.height

    def to_array(self) -> np.ndarray:
        return np.array(
            [
                [self.x, self.y],
                [self.x + self.width, self.y],
                [self.x + self.width, self.y + self.height],
                [self.x, self.y + self.height],
            ]
        )

    @property
    def center(self) -> Pos:
        return Pos(self.x_middle, self.y_middle)

    @property
    def x_middle(self) -> int:
        return self.x + self.width // 2

    @property
    def y_middle(self) -> int:
        return self.y + self.height // 2

    @property
    def top_left(self) -> Pos:
        return Pos(self.left, self.top)

    @property
    def top_right(self) -> Pos:
        return Pos(self.right, self.top)

    @property
    def bottom_left(self) -> Pos:
        return Pos(self.left, self.bottom)

    @property
    def bottom_right(self) -> Pos:
        return Pos(self.right, self.bottom)

    @property
    def left(self) -> int:
        return self.x

    @property
    def right(self) -> int:
        return self.x + self.width

    @property
    def top(self) -> int:
        return self.y

    @property
    def bottom(self) -> int:
        return self.y + self.height

    @staticmethod
    def aabb_algorithm(rect_1: "Rect", rect_2: "Rect") -> bool:
        def check(rect_1: Rect, rect_2: Rect) -> bool:
            return (
                rect_1.left <= rect_2.right
                and rect_1.right >= rect_2.left
                and rect_1.top <= rect_2.bottom
                and rect_1.bottom >= rect_2.top
            )

        return check(rect_1, rect_2) or check(rect_2, rect_1)
