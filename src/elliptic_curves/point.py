from typing import Any, Literal

import sympy
from sympy import Rational


class Point:
    def __init__(self, value: tuple[Rational, Rational] | Literal["O"]):
        self._value = value

    @property
    def value(self) -> tuple[Rational, Rational] | Literal["O"]:
        return self._value

    @property
    def x(self) -> sympy.Rational:
        assert self.value != "O"
        return self.value[0]

    @property
    def y(self) -> sympy.Rational:
        assert self.value != "O"
        return self.value[1]

    def is_integer(self) -> bool:
        if self.is_neutral_element():
            return True
        return self.x.is_Integer and self.y.is_Integer

    def is_neutral_element(self) -> bool:
        return self.value == "O"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.value == other.value
        return False

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash(self.value)


O = Point("O")
