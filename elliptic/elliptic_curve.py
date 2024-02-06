from typing import Union, Tuple, List, Any, Optional, Literal, Type
import sympy


class Point:
    def __init__(
        self, value: Union[Tuple[sympy.Rational, sympy.Rational], Literal["O"]]
    ):
        self.value = value

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
            return False
        return self.x.is_Integer and self.y.is_Integer

    def is_neutral_element(self) -> bool:
        return self.value == "O"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.value == other.value
        return False

    def __str__(self) -> str:
        return str(self.value)


class SingularCurveError(Exception):
    pass


class EllipticCurve:
    def __init__(self, a: int, b: int):
        """Creates an ellptic curve given by: y^2 = x^3 + ax + b"""
        self.a, self.b = a, b
        self.discriminant = 4 * a**3 + 27 * b**2
        if self.discriminant == 0:
            raise SingularCurveError("Invalid coefficients for the elliptic curve!")

    def inv(self, p: Point):
        if p.value == "O":
            return Point("O")
        return Point((p.x, -p.y))

    def sum(self, p_1: Point, p_2: Point) -> Point:
        if p_1.value == "O":
            return p_2
        if p_2.value == "O":
            return p_1
        if p_1 == self.inv(p_2):
            return Point("O")
        if p_1 == p_2:
            u = (3 * p_1.x**2 + self.a) / (2 * p_1.y)
            v = p_1.y - u * p_1.x
            x = u**2 - 2 * p_1.x
            y = u * x + v
            return Point((x, -y))
        u = (p_1.y - p_2.y) / (p_1.x - p_2.x)
        v = p_1.y - u * p_1.x
        x = u**2 - p_1.x - p_2.x
        y = u * x + v
        return Point((x, -y))

    def __str__(self):
        return f"y^2 = x^2 + {self.a}x + {self.b}"
