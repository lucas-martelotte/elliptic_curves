from typing import Any, Literal, Tuple, Union

import sympy


class SingularCurveError(Exception):
    pass


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


class EllipticCurve:
    def __init__(self, a: int, b: int):
        """Creates an ellptic curve given by: y^2 = x^3 + ax + b"""
        self.a, self.b = a, b
        self.discriminant = 4 * a**3 + 27 * b**2
        if self.discriminant == 0:
            raise SingularCurveError("Invalid coefficients for the elliptic curve!")

    def inv(self, p: Point) -> Point:
        """Calculates the inverse of p"""
        if p.value == "O":
            return Point("O")
        return Point((p.x, -p.y))

    def sum(self, p_1: Point, p_2: Point) -> Point:
        """Operates the points p_1 and p_2"""
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
        x, y = sympy.symbols("x, y")
        exp = x**2 + self.a * x + self.b
        exp_str = str(exp).replace("**", "^").replace("*", "")
        return f"E : y^2 = {exp_str}"
